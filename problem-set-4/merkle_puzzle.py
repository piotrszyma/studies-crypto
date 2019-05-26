import sys
import os
import random
import functools
import itertools
import collections
import argparse
import time
import multiprocessing

sys.path.append(os.path.abspath('../problem-set-3'))

from typing import List

from Crypto.Cipher import AES
import Crypto
from Crypto.Util import Padding

C_PARAM = 1
KEY_SIZE = 16
N = 2 ** 24 # number of puzzles
KNOWN_PART = os.urandom(15)

KEY_ID_LEN = 48 # Confirms good key_id len


def get_full_key(known_part):
  return known_part + os.urandom(16 - len(known_part))

def encrypt(message, secret):
  iv = os.urandom(16)
  padded_message = Padding.pad(message, 16)
  aes_obj = AES.new(secret, AES.MODE_CBC, iv)
  cypher = aes_obj.encrypt(padded_message)
  return cypher + iv

def decrypt(message, secret):
  cypher, iv = message[:-16], message[-16:]
  aes_obj = AES.new(secret, AES.MODE_CBC, iv)
  message = aes_obj.decrypt(cypher)
  return Padding.unpad(message, 16)

KeyEncryption = collections.namedtuple('KeyEncryption', 'key encryption')

def generate_single_puzzle(puzzle_id, k1, k2, constant):
  puzzle_id_bytes = puzzle_id.to_bytes(16, byteorder='big')
  key_id = encrypt(puzzle_id_bytes, k1)
  key = encrypt(key_id, k2)
  # id, key, constant
  enc_key = get_full_key(KNOWN_PART)
  # CONST ; KEY; ID
  msg = key_id + key + constant
  encryption = encrypt(msg, enc_key)
  return key_id, KeyEncryption(key, encryption)


def generate_puzzles() -> (List[bytes], bytes, bytes):
  """Generates puzzle

  Returns:
      Tuple with list of puzzles, k2 and constant.
  """
  k1 = os.urandom(16)
  k2 = os.urandom(16)
  constant = os.urandom(KEY_SIZE // 4)
  puzzles = []
  args_map = ((puzzle_id, k1, k2, constant) for puzzle_id in range(N))
  with multiprocessing.Pool(processes=3) as pool:
    puzzles = dict(pool.starmap(generate_single_puzzle, args_map))
  return puzzles, constant


def _get_possible_keys(size):
  return (
    num.to_bytes(length=size, byteorder='big')
    for num in range(1, (2 ** 8) ** size))


def choose_decrypt_and_return_id(puzzles, constant):
  chosen_puzzle = random.choice(puzzles)

  size = KEY_SIZE - len(KNOWN_PART)
  for possible_unknown_key_part in _get_possible_keys(size):
    possible_key = KNOWN_PART + possible_unknown_key_part
    try:
      decrypted = decrypt(chosen_puzzle, possible_key)
    except ValueError:
      pass
    else:
      key_id_key, decrypted_constant = decrypted[:-len(constant)], decrypted[-len(constant):]

      if constant == decrypted_constant:
        key_id = key_id_key[:KEY_ID_LEN]
        key = key_id_key[KEY_ID_LEN:]
        break

  return key_id, key


def main():
  # Sender.
  print(f'Size: {N}')
  start = time.time()
  id_to_key_enc, constant = generate_puzzles()
  puzzles = [key_enc.encryption
             for key_enc in id_to_key_enc.values()]
  generated = time.time()
  print(f'Generated in {(generated - start):.2f}s')
  # Receiver.

  chosen_key_id, chosen_key = choose_decrypt_and_return_id(puzzles, constant)
  cracked = time.time() - generated

  print(f'Cracked in {cracked:.2f}s')
  # Checks if receiver has good key.
  # (sender has same key under chosen_key_id)
  assert id_to_key_enc[chosen_key_id].key == chosen_key

if __name__ == "__main__":
  main()
