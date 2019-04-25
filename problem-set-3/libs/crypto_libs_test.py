import unittest
import random

import parameterized

from libs import crypto_libs
from libs import utils
from config import settings


ALL_MODES = [
    'aes-128-cbc', 'aes-128-cfb', 'aes-128-cfb1', 'aes-128-cfb8',
    'aes-128-ctr', 'aes-128-ecb', 'aes-128-gcm', 'aes-128-ofb', 'aes-128-xts',
    'aes-192-cbc', 'aes-192-cfb', 'aes-192-cfb1', 'aes-192-cfb8',
    'aes-192-ctr', 'aes-192-ecb', 'aes-192-gcm', 'aes-192-ofb', 'aes-256-cbc',
    'aes-256-cfb', 'aes-256-cfb1', 'aes-256-cfb8', 'aes-256-ctr',
    'aes-256-ecb', 'aes-256-gcm', 'aes-256-ofb', 'aes-256-xts', 'aes128',
    'aes192', 'aes256', 'bf', 'bf-cbc', 'bf-cfb', 'bf-ecb', 'bf-ofb',
    'blowfish', 'camellia-128-cbc', 'camellia-128-cfb', 'camellia-128-cfb1',
    'camellia-128-cfb8', 'camellia-128-ecb', 'camellia-128-ofb',
    'camellia-192-cbc', 'camellia-192-cfb', 'camellia-192-cfb1',
    'camellia-192-cfb8', 'camellia-192-ecb', 'camellia-192-ofb',
    'camellia-256-cbc', 'camellia-256-cfb', 'camellia-256-cfb1',
    'camellia-256-cfb8', 'camellia-256-ecb', 'camellia-256-ofb', 'camellia128',
    'camellia192', 'camellia256', 'cast', 'cast-cbc', 'cast5-cbc', 'cast5-cfb',
    'cast5-ecb', 'cast5-ofb', 'chacha', 'des', 'des-cbc', 'des-cfb',
    'des-cfb1', 'des-cfb8', 'des-ecb', 'des-ede', 'des-ede-cbc', 'des-ede-cfb',
    'des-ede-ofb', 'des-ede3', 'des-ede3-cbc', 'des-ede3-cfb', 'des-ede3-cfb1',
    'des-ede3-cfb8', 'des-ede3-ofb', 'des-ofb', 'des3', 'desx', 'desx-cbc',
    'gost89', 'gost89-cnt', 'gost89-ecb', 'id-aes128-GCM', 'id-aes192-GCM',
    'id-aes256-GCM', 'rc2', 'rc2-40-cbc', 'rc2-64-cbc', 'rc2-cbc', 'rc2-cfb',
    'rc2-ecb', 'rc2-ofb', 'rc4', 'rc4-40', 'rc4-hmac-md5'
]

UNSUPPORTED_MODS = [
  'des-ede3-cfb1',
  'aes-128-xts',
  'aes-256-xts',
  'id-aes128-GCM',
  'id-aes192-GCM',
  'id-aes256-GCM',
  'aes-128-gcm',
  'aes-192-gcm',
  'aes-256-gcm',
]

TESTED_MODES = set(ALL_MODES) - set(UNSUPPORTED_MODS)

def random_bytes(bytes_size):
  return bytes(random.getrandbits(8) for _ in range(bytes_size))

def increment_bytes(bytes_number):
  length = len(bytes_number)
  incremented_int = int.from_bytes(bytes_number, byteorder='big') + 1
  return incremented_int.to_bytes(length, byteorder='big')

def xor_bytes(left, right):
  return bytes(left_byte ^ right_byte for left_byte, right_byte in zip(left, right))


class CryptoLibsTests(unittest.TestCase):

  def setUp(self):
    self.message = b'test data'
    self.password = b'test password'
    self.secret = b'test secret'

  def encrypt_in_mode(self, mode):
    return crypto_libs.encrypt(self.message, self.secret, self.password, mode)

  def decrypt_in_mode(self, encryption, mode):
    return crypto_libs.decrypt(encryption, self.secret, self.password, mode)

  @parameterized.parameterized.expand(TESTED_MODES)
  def test_encryption_modes(self, tested_mode):
    encrypted_data = self.encrypt_in_mode(tested_mode)
    decrypted_data = self.decrypt_in_mode(encrypted_data, tested_mode)
    self.assertEqual(self.message, decrypted_data)

  def test_aes_cbc_encrypt_crack(self):
    mode = 'aes-128-cbc'
    iv_0 = random_bytes(16)
    key = random_bytes(16)
    msg_0 = random_bytes(16)

    cypher_0 = crypto_libs.encrypt_nopad(msg_0, key, iv_0, mode)

    iv_1 = increment_bytes(iv_0)
    will_use_random = random.choices((True, False))
    if will_use_random:
      msg_1 = random_bytes(16)
    else:
      msg_1 = xor_bytes(xor_bytes(msg_0, iv_0), iv_1)

    cypher_1 = crypto_libs.encrypt_nopad(msg_1, key, iv_1, mode)

    if cypher_0 == cypher_1 and will_use_random:
      self.fail('Same cyphers different output!')
