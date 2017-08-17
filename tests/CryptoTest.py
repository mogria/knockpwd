import unittest
from knockpwd.Crypto import Crypto
from Crypto import Random

class CryptoTest(unittest.TestCase):

    def setUp(self):
        # 32 bytes required for aes256
        self.key       = b"12345678901234567890123456789012"
        self.wrong_key = b"an other key12345678901234567890"
        self.message   = b"test message"
        self.iv        = Random.new().read(Crypto.BLOCK_SIZE)
        self.fake_iv   = "i" * Crypto.BLOCK_SIZE
        self.fake_crypted = "c" * (Crypto.BLOCK_SIZE * 10)
        self.fake_sig  = "s" * Crypto.DIGEST_SIZE
        self.fake_encrypted = self.fake_iv + self.fake_crypted + self.fake_sig 

    def tearDown(self):
        pass

    def test_pad_simple(self): 
        yield self.check_pad_simple, ("a" * Crypto.BLOCK_SIZE,)
        yield self.check_pad_simple, ("b" * (Crypto.BLOCK_SIZE + 1),)
        yield self.check_pad_simple, ("c" * (Crypto.BLOCK_SIZE + 7),)
        yield self.check_pad_simple, ("d" * (Crypto.BLOCK_SIZE * 2 - 1),)

    def check_pad_simple(self, message):
        self.assertEqual(Crypto.BLOCK_SIZE * 2, len(Crypto.pad(message)))

    
    def test_extract_iv(self):
        self.assertEqual(self.fake_iv, Crypto.extract_iv(self.fake_encrypted))

    def test_extract_signature(self):
        self.assertEqual(self.fake_sig, Crypto.extract_signature(self.fake_encrypted))

    def test_extract_crypted(self):
        self.assertEqual(self.fake_crypted, Crypto.extract_crypted(self.fake_encrypted))

    def test_sign(self):
        sig = Crypto.sign(b"test", self.key)
        self.assertEqual(bytes, sig.__class__)
        sig2 = Crypto.sign(b"tesa", self.key)
        self.assertEqual(bytes, sig2.__class__)
        self.assertNotEqual(sig, sig2, 'signatures for two different strings should return different values')

    def test_verify(self):
        sig = Crypto.sign(self.message, self.key)
        self.assertTrue(Crypto.verify(self.message, self.key, sig))

    def test_verify_fail_wrong_key(self):
        sig = Crypto.sign(self.message, self.key)
        self.assertFalse(Crypto.verify(self.message, self.wrong_key, sig))

    def test_verify_fail_wrong_message(self):
        sig = Crypto.sign(self.message, self.key)
        self.assertFalse(Crypto.verify(self.message + b"2", self.key, sig))

    def test_verify_fail_wrong_signature(self):
        sig = Crypto.sign(self.message, self.wrong_key)
        self.assertFalse(Crypto.verify(self.message + b"2", self.key, sig))

    def test_encrypt_same_iv(self):
        enc1 = Crypto.encrypt(self.message, self.key, iv=self.iv)
        enc2 = Crypto.encrypt(self.message, self.key, iv=self.iv)
        self.assertEqual(bytes, enc1.__class__)
        self.assertEqual(bytes, enc2.__class__)
        self.assertEqual(enc1, enc2)

    def test_encrypt_same_iv_different_message(self):
        enc1 = Crypto.encrypt(self.message + b"a", self.key, iv=self.iv)
        enc2 = Crypto.encrypt(self.message + b"b", self.key, iv=self.iv)
        self.assertEqual(bytes, enc1.__class__)
        self.assertEqual(bytes, enc2.__class__)
        self.assertNotEqual(enc1, enc2)

    def test_encrypt_different_key(self):
        enc1 = Crypto.encrypt(self.message, self.key, iv=self.iv)
        enc2 = Crypto.encrypt(self.message, self.wrong_key, iv=self.iv)
        self.assertEqual(bytes, enc1.__class__)
        self.assertEqual(bytes, enc2.__class__)
        self.assertNotEqual(enc1, enc2)


