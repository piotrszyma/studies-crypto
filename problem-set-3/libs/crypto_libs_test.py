import random
import unittest

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


class Oracle:

  def __init__(self):
    self.key = utils.random_bytes(16)
    self.iv = utils.random_bytes(16)
    self.mode = 'aes-128-cbc'

  def get_cypher(self, msg):
    cypher = crypto_libs.encrypt(msg, self.key, self.mode, iv=self.iv)
    self.iv = utils.increment_bytes(self.iv)
    return cypher

  def challenge(self, msg):
    use_random_msg = random.getrandbits(1)
    if use_random_msg:
      print('oracle used random msg')
      msg = utils.random_bytes(16)
    else:
      print('oracle used adversary')
    return self.get_cypher(msg)


class CryptoLibsTests(unittest.TestCase):

  def setUp(self):
    super().setUp()
    self.message = b'test data'
    self.secret = b'test secret'

  def encrypt_in_mode(self, mode):
    return crypto_libs.encrypt(self.message, self.secret, mode)

  def decrypt_in_mode(self, encryption, mode):
    return crypto_libs.decrypt(encryption, self.secret,  mode)

  @parameterized.parameterized.expand(TESTED_MODES)
  def test_encryption_modes(self, tested_mode):
    encrypted_data = self.encrypt_in_mode(tested_mode)
    decrypted_data = self.decrypt_in_mode(encrypted_data, tested_mode)
    self.assertEqual(self.message, decrypted_data)

  def test_cpa_insecure(self):
    oracle = Oracle()

    msg0 = utils.random_bytes(16)
    c0 = oracle.get_cypher(msg0)

    iv0 = c0[-16:]
    calculated_iv1 = utils.increment_bytes(iv0)

    msg1 = utils.xor_bytes(utils.xor_bytes(msg0, iv0), calculated_iv1)

    c0_without_iv = c0[:-16]
    received_msg1 = oracle.challenge(msg1)[:-16]

    if c0_without_iv == received_msg1:
      print('Adversary: used my message')
    else:
      print('Adversary: Used random message')
