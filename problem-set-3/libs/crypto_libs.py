import subprocess
import random
import pathlib
import os

from typing import Text, List

from config import settings
from libs import utils

SIZE_OF_IV = 16

def get_random_iv():
  return bytes(random.randrange(0, 255) for _ in range(SIZE_OF_IV))

def encrypt(data: bytes, secret: bytes, mode: Text, iv: bytes = None) -> bytes:
  iv = iv or get_random_iv()
  command = ' '.join(f"""
    openssl
    enc
    -e
    -{mode}
    -K {utils.hex_from_bytes(secret)}
    -iv {utils.hex_from_bytes(iv)}
  """.split())
  process = subprocess.run(['bash', '-c', command],
                           input=data,
                           stdout=subprocess.PIPE)
  return process.stdout + iv


def decrypt(data: bytes, secret: bytes, mode: Text):
  iv = data[-SIZE_OF_IV:]
  data = data[:-SIZE_OF_IV]
  command = ' '.join(f"""
    openssl
    enc
    -d
    -{mode}
    -K {utils.hex_from_bytes(secret)}
    -iv {utils.hex_from_bytes(iv)}
  """.split())
  process = subprocess.run(['bash', '-c', command],
                           input=data,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
  if process.stderr:
    return os.urandom(16)
    # import pdb; pdb.set_trace()
    # raise RuntimeError(f'Mode {mode} returned error: "{process.stderr}"')
  return process.stdout
