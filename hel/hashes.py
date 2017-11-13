import hashlib
from hel.settings import SECRET_KEY

def sha512(data):
    byte_string = bytes(data + SECRET_KEY, 'utf-8')
    return hashlib.sha512(byte_string).hexdigest()
