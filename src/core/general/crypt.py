"""
  Author:
  Create date:
  Description:    Provide encryption and decryption function for sensitive data


  Version     Date                Description(of Changes)
  1.0                             Created
"""

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from core.general import settings


class Encryption():
    """
        Class to encrypt and decrypt a string
    """

    def __init__(self):
        """
            Galib
        """
        key_path = settings.PROJECT_ROOT_PATH + '/etc/key.txt'
        with open(key_path, 'r') as key_file:
            key = key_file.read()
        self.key = str.encode(key)

    def encrypt(self, source, encode=True):
        """
            encryp the source string and return encrypted string
        """
        source = str.encode(source)
        # use SHA-256 over our key to get a proper-sized AES key
        key = SHA256.new(self.key).digest()
        ivstring = Random.new().read(AES.block_size)  # generate IV
        encryptor = AES.new(key, AES.MODE_CBC, ivstring)
        # calculate needed padding
        padding = AES.block_size - len(source) % AES.block_size
        # Python 2.x: source += chr(padding) * padding
        source += bytes([padding]) * padding
        # store the IV at the beginning and encrypt
        data = ivstring + encryptor.encrypt(source)
        return base64.b64encode(data).decode("latin-1") if encode else data


    def decrypt(self, source, decode=True):
        """
            decrypt the source string and return decrypted string
        """
        if decode:
            source = base64.b64decode(source.encode("latin-1"))
        # use SHA-256 over our key to get a proper-sized AES key
        key = SHA256.new(self.key).digest()
        ivstring = source[:AES.block_size]  # extract the IV from the beginning
        decryptor = AES.new(key, AES.MODE_CBC, ivstring)
        data = decryptor.decrypt(source[AES.block_size:])  # decrypt
        # pick the padding value from the end; Python 2.x: ord(data[-1])
        padding = data[-1]
        # Python 2.x: chr(padding) * padding
        if data[-padding:] != bytes([padding]) * padding:
            raise ValueError("Invalid padding...")
        returnValue = data[:-padding]  # remove the padding
        return returnValue.decode()
