from libknockpw.Crypto import Crypto
from Crypto import Random
from nose.tools import *

class TestCrypto:
    key       = b"12345678901234567890123456789012"
    wrong_key = b"an other key12345678901234567890"
    message   = b"test message"
    iv        = Random.new().read(Crypto.BLOCK_SIZE)
    fake_iv   = "i" * Crypto.BLOCK_SIZE
    fake_crypted = "c" * (Crypto.BLOCK_SIZE * 10)
    fake_sig  = "s" * Crypto.DIGEST_SIZE
    fake_encrypted = fake_iv + fake_crypted + fake_sig 

    def tearDown(self):
        pass

    def test_pad(self): 
        yield self.check_pad, self.message
        yield self.check_unpad, self.message
        for i in range(Crypto.BLOCK_SIZE, Crypto.BLOCK_SIZE * 8 + 2, 3):
            yield self.check_pad, b"a" * i
            yield self.check_unpad, b"a" * i

    def check_pad(self, message):
        padded_message = Crypto.pad(message)
        assert_greater_equal(len(padded_message), len(padded_message))
        assert_equal(0, len(padded_message) % Crypto.BLOCK_SIZE)

    def check_unpad(self, padded_message): 
        assert_equal(padded_message, Crypto.unpad(Crypto.pad(padded_message)))

    
    def test_extract_iv(self):
        assert_equal(self.fake_iv, Crypto.extract_iv(self.fake_encrypted))

    def test_extract_signature(self):
        assert_equal(self.fake_sig, Crypto.extract_signature(self.fake_encrypted))

    def test_extract_crypted(self):
        assert_equal(self.fake_crypted, Crypto.extract_crypted(self.fake_encrypted))

    def test_sign(self):
        sig = Crypto.sign(b"test", self.key)
        assert_equal(bytes, sig.__class__)
        sig2 = Crypto.sign(b"tesa", self.key)
        assert_equal(bytes, sig2.__class__)
        assert_not_equal(sig, sig2, 'signatures for two different strings should return different values')

    def test_verify(self):
        sig = Crypto.sign(self.message, self.key)
        assert_true(Crypto.verify(self.message, self.key, sig))

    def test_verify_fail_wrong_key(self):
        sig = Crypto.sign(self.message, self.key)
        assert_false(Crypto.verify(self.message, self.wrong_key, sig))

    def test_verify_fail_wrong_message(self):
        sig = Crypto.sign(self.message, self.key)
        assert_false(Crypto.verify(self.message + b"2", self.key, sig))

    def test_verify_fail_wrong_signature(self):
        sig = Crypto.sign(self.message, self.wrong_key)
        assert_false(Crypto.verify(self.message + b"2", self.key, sig))

    def test_encrypt_same_iv(self):
        enc1 = Crypto.encrypt(self.message, self.key, iv=self.iv)
        enc2 = Crypto.encrypt(self.message, self.key, iv=self.iv)
        assert_equal(bytes, enc1.__class__)
        assert_equal(bytes, enc2.__class__)
        assert_equal(enc1, enc2)

    def test_encrypt_same_iv_different_message(self):
        enc1 = Crypto.encrypt(self.message + b"a", self.key, iv=self.iv)
        enc2 = Crypto.encrypt(self.message + b"b", self.key, iv=self.iv)
        assert_equal(bytes, enc1.__class__)
        assert_equal(bytes, enc2.__class__)
        assert_not_equal(enc1, enc2)

    def test_encrypt_different_key(self):
        enc1 = Crypto.encrypt(self.message, self.key, iv=self.iv)
        enc2 = Crypto.encrypt(self.message, self.wrong_key, iv=self.iv)
        assert_equal(bytes, enc1.__class__)
        assert_equal(bytes, enc2.__class__)
        assert_not_equal(enc1, enc2)

    def test_decrypt(self):
        result = Crypto.decrypt(Crypto.encrypt(self.message, self.key), self.key)
        assert_equal(result, self.message)

    def test_decrypt_wrong_key(self):
        assert_equal(None, Crypto.decrypt(Crypto.encrypt(self.message, self.key), self.wrong_key))

    def test_generate_key(self):
        key = Crypto.generate_key()
        assert_equals(Crypto.KEY_SIZE, len(key))
        assert_is_instance(key, bytes)
