from binascii import hexlify, unhexlify
from ecdsa import SigningKey, VerifyingKey
from ecdsa.util import PRNG
from ecdsa.curves import SECP256k1
from hashlib import sha256
from mnemonic import Mnemonic

mnemo = Mnemonic("english")


class Wallet:
    def __init__(self, seed_phrase=None):

        if seed_phrase == None:
            seed_phrase = generate_seed_phrase()

        self.private_key = generate_private_key(seed_phrase)
        self.public_key = generate_public_key(self.private_key)
        self.address = generate_address(self.public_key)


def generate_seed_phrase():

    words = mnemo.generate(strength=192)

    print(words)

    return words


def generate_private_key(seed_phrase):

    seed = mnemo.to_seed(seed_phrase)

    rng = PRNG(seed)

    sk = SigningKey.generate(curve=SECP256k1, entropy=rng)

    return hexlify(sk.to_string()).decode('ascii')


def generate_public_key(private_key):
    private_key = unhexlify(private_key)

    sk = SigningKey.from_string(string=private_key, curve=SECP256k1)

    vk = sk.verifying_key

    return hexlify(vk.to_string()).decode('ascii')


def generate_address(public_key):
    payload = unhexlify(public_key)

    digest = sha256(payload).hexdigest()

    digest_last20 = digest[-40:]

    address = "0x" + digest_last20

    return address


def recover_public_keys(signature, hash):
    vks = VerifyingKey.from_public_key_recovery(signature, hash, SECP256k1)

    return vks


def verify_signature(signature, hash, address):
    vks = recover_public_keys(signature, hash)

    try:
        vks[0].verify(signature, hash)

        pk0 = hexlify(vks[0].to_string()).decode('ascii')

        address0 = generate_address(pk0)

        if address0 == address:
            return True
    except:
        pass

    try:
        vks[1].verify(signature, hash)

        pk1 = hexlify(vks[1].to_string()).decode('ascii')

        address1 = generate_address(pk1)

        if address1 == address:
            return True

    except:
        return False


def json_construct_wallet(wallet: Wallet):
    return {
        "private_key": wallet.private_key,
        "public_key": wallet.public_key,
        "address": wallet.address
    }


def json_retrieve_private_key(json_wallet: dict):
    private_key_str = unhexlify(json_wallet["private_key"])

    sk = SigningKey.from_string(string=private_key_str, curve=SECP256k1)

    return sk


def json_retrieve_public_key(json_wallet: dict):
    public_key_str = unhexlify(json_wallet["public_key"])

    vk = VerifyingKey.from_string(string=public_key_str, curve=SECP256k1)

    return vk


def json_retrieve_address(json_wallet: dict):
    address = json_wallet["address"]

    return address
