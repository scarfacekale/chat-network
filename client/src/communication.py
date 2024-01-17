import base64

# xbps-install python3-cryptography python3-pycryptodome python3-argon2
# pip3 install pycrypto pycryptodome pycryptodomex

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import \
        Ed25519PublicKey, Ed25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

class Sender:

    def __init__(self):
        self.identity_key = X25519PrivateKey.generate()
        self.signed_prekey = X25519PrivateKey.generate()
        self.onetime_prekey = X25519PrivateKey.generate()

        self.shared_key = None

    @property
    def ik_public(self):
        return self.identity_key.public_key()

    @property
    def spk_public(self):
        return self.signed_prekey.public_key()

    @property
    def opk_public(self):
        return self.onetime_prekey.public_key()

    @property
    def ik_public_bytes(self):
        return self.ik_public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    @property
    def spk_public_bytes(self):
        return self.spk_public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    @property
    def opk_public_bytes(self):
        return self.opk_public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    def x3dh(self, identity_key, epheremal_key, length=32):

        identity_key = x25519.X25519PublicKey.from_public_bytes(identity_key)
        epheremal_key = x25519.X25519PublicKey.from_public_bytes(epheremal_key)

        dh1 = self.signed_prekey.exchange(identity_key)
        dh2 = self.identity_key.exchange(epheremal_key)
        dh3 = self.signed_prekey.exchange(epheremal_key)
        dh4 = self.onetime_prekey.exchange(epheremal_key)

        hkdf = HKDF(algorithm=hashes.SHA256(), 
            length=length, 
            salt=b'',
            info=b'', 
            backend=default_backend()
        )

        self.shared_key = hkdf.derive(dh1 + dh2 + dh3 + dh4)

    def encrypt(self, message):
        nonce = get_random_bytes(24)

        cipher = ChaCha20.new(
            key=self.shared_key,
            nonce=nonce
        )

        return cipher.encrypt(message.encode()), nonce

    def decrypt(self, message, nonce):
        cipher = ChaCha20.new(
            key=self.shared_key,
            nonce=nonce
        )

        return cipher.decrypt(message).decode()

class Receiver:

    def __init__(self):
        self.identity_key = X25519PrivateKey.generate()
        self.epheremal_key = X25519PrivateKey.generate()

        self.shared_key = None

    @property
    def ik_public(self):
        return self.identity_key.public_key()

    @property
    def epk_public(self):
        return self.epheremal_key.public_key()

    @property
    def ik_public_bytes(self):
        return self.ik_public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    @property
    def epk_public_bytes(self):
        return self.epk_public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    # backwards exchange of sender
    def x3dh(self, identity_key, signed_prekey, onetime_prekey, length=32):

        identity_key = x25519.X25519PublicKey.from_public_bytes(identity_key)
        signed_prekey = x25519.X25519PublicKey.from_public_bytes(signed_prekey)
        onetime_prekey = x25519.X25519PublicKey.from_public_bytes(onetime_prekey)

        dh1 = self.identity_key.exchange(signed_prekey)
        dh2 = self.epheremal_key.exchange(identity_key)
        dh3 = self.epheremal_key.exchange(signed_prekey)
        dh4 = self.epheremal_key.exchange(onetime_prekey)

        hkdf = HKDF(algorithm=hashes.SHA256(), 
            length=length, 
            salt=b'',
            info=b'', 
            backend=default_backend()
        )

        self.shared_key = hkdf.derive(dh1 + dh2 + dh3 + dh4)

    def encrypt(self, message):
        nonce = get_random_bytes(24)

        cipher = ChaCha20.new(
            key=self.shared_key,
            nonce=nonce
        )

        return cipher.encrypt(message.encode()), nonce

    def decrypt(self, message, nonce):
        cipher = ChaCha20.new(
            key=self.shared_key,
            nonce=nonce
        )

        return cipher.decrypt(message).decode()
