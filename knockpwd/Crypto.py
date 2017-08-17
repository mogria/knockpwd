import hmac
from Crypto.Cipher import AES
from Crypto import Random

class Crypto:
    DIGEST = 'sha512'
    DIGEST_SIZE = int(512 / 8)
    BLOCK_SIZE = 16

    @staticmethod
    def extract_iv(encrypted):
        return encrypted[0:Crypto.BLOCK_SIZE]

    @staticmethod
    def extract_signature(encrypted):
        return encrypted[-Crypto.DIGEST_SIZE:]

    @staticmethod
    def extract_crypted(encrypted):
        return encrypted[Crypto.BLOCK_SIZE:-Crypto.DIGEST_SIZE]

    @staticmethod
    def pad(msg):
        required_padding = Crypto.BLOCK_SIZE - (len(msg) % Crypto.BLOCK_SIZE)
        return msg + (required_padding * chr(required_padding)).encode('ascii')

    @staticmethod
    def unpad(msg):
        last_byte = msg[len(msg) - 1]
        return msg[:-last_byte]

    @staticmethod
    def encrypt(msg, key, iv=None):
        if iv is None:
            iv = Random.new().read(Crypto.BLOCK_SIZE)

        aes = AES.new(key, AES.MODE_CBC, iv)
        encrypted = aes.encrypt(Crypto.pad(msg))
        return iv + encrypted + Crypto.sign(iv + encrypted, key)

    @staticmethod
    def decrypt(encrypted, key):
        iv = Crypto.extract_iv(encrypted)
        crypted = Crypto.extract_crypted(encrypted)
        signature = Crypto.extract_signature(encrypted)
        if not Crypto.verify(iv + crypted, key, signature):
            return None

        aes = AES.new(key, AES.MODE_CBC, iv)
        return Crypto.unpad(aes.decrypt(crypted))

    @staticmethod
    def sign(msg, key):
        h = hmac.new(msg=msg, key=key, digestmod='sha512')
        return h.digest()

    @staticmethod
    def verify(msg, key, expected_sig):
        return hmac.compare_digest(Crypto.sign(msg, key), expected_sig)

