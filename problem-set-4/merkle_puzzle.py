import sys
import os
import random
import functools
import collections
import argparse

sys.path.append(os.path.abspath('../problem-set-3'))

from typing import List

from libs.crypto_libs import encrypt, decrypt

encrypt = functools.partial(encrypt, mode='aes-128-cbc')
decrypt = functools.partial(decrypt, mode='aes-128-cbc')

C_PARAM = 10
KEY_SIZE = 16
N = 2 ** 24 # number of puzzles
KNOWN_PART = os.urandom(15)

KEY_ID_LEN = 48 # Confirms good key_id len


def get_full_key(known_part):
  return known_part + os.urandom(16 - len(known_part))


KeyEncryption = collections.namedtuple('KeyEncryption', 'key encryption')

def generate_single_puzzle(puzzle_id, k1, k2, constant):
  puzzle_id_bytes = puzzle_id.to_bytes(16, byteorder='big')
  key_id = encrypt(puzzle_id_bytes, k1)
  assert KEY_ID_LEN == len(key_id)
  key = encrypt(key_id, k2)
  # id, key, constant
  enc_key = get_full_key(KNOWN_PART)
  # CONST ; KEY; ID
  msg = key_id + key + constant
  # print(len(key_id))
  encryption = encrypt(msg, enc_key)
  return key_id, KeyEncryption(key, encryption)


def generate_puzzles() -> (List[bytes], bytes, bytes):
  """Generates puzzle

  Returns:
      Tuple with list of puzzles, k2 and constant.
  """
  # constant = os.urandom()
  k1 = os.urandom(16)
  k2 = os.urandom(16)
  constant = os.urandom(KEY_SIZE // 4)
  puzzles = dict(
      generate_single_puzzle(
          puzzle_id,
          k1,
          k2,
          constant
      ) for puzzle_id in range(N)
  )
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
    except RuntimeError:
      pass

    key_id_key, decrypted_constant = decrypted[:-len(constant)], decrypted[-len(constant):]

    if constant == decrypted_constant:
      key_id = key_id_key[:KEY_ID_LEN]
      key = key_id_key[KEY_ID_LEN:]
      break

  return key_id, key


def main():
  # Sender.
  id_to_key_enc, constant = generate_puzzles()
  print('Puzzle generated.')
  puzzles = [key_enc.encryption
             for key_enc in id_to_key_enc.values()]

  # Receiver.
  chosen_key_id, chosen_key = choose_decrypt_and_return_id(puzzles, constant)

  # Checks if receiver has good key.
  # (sender has same key under chosen_key_id)
  assert id_to_key_enc[chosen_key_id].key == chosen_key

if __name__ == "__main__":
  main()
