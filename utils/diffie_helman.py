from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

parameters = dh.generate_parameters(generator=2, key_size=2048)

private_key = parameters.generate_private_key()

peer_public_key = parameters.generate_private_key().public_key()

shared_key = private_key.exchange(peer_public_key)

# Perform key derivation.

derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(shared_key)

private_key_2 = parameters.generate_private_key()

peer_public_key_2 = parameters.generate_private_key().public_key()

shared_key_2 = private_key_2.exchange(peer_public_key_2)

derived_key_2 = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(shared_key_2)
