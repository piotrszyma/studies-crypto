import subprocess
import random

from typing import Text, List

from config import settings
from libs import utils


def encrypt(data: bytes, secret: bytes, password: bytes, mode: Text) -> bytes:
  command = ' '.join(f"""
    openssl
    enc
    -e
    -{mode}
    -e
    -K {utils.hex_from_bytes(secret)}
    -k {utils.hex_from_bytes(password)}
  """.split())
  process = subprocess.run(['bash', '-c', command],
                           input=data,
                           stdout=subprocess.PIPE)
  return process.stdout


def decrypt(data: bytes, secret: bytes, password: bytes, mode: Text):
  command = ' '.join(f"""
    openssl
    enc
    -d
    -{mode}
    -K {utils.hex_from_bytes(secret)}
    -k {utils.hex_from_bytes(password)}
  """.split())
  process = subprocess.run(['bash', '-c', command],
                           input=data,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
  if process.stderr:
    raise RuntimeError(f'Mode {mode} returned error {process.stderr}')
  return process.stdout

def encrypt_many(data: List[bytes], secret: bytes, password: bytes, mode: Text) -> List[bytes]:
  return [encrypt(chunk) for chunk in data]

def encrypt_challenge(messages: List[bytes], secret: bytes, password: bytes, mode: Text):
  return random.choice(messages)

def encrypt_nopad(data: bytes, secret: bytes, iv: bytes, mode: Text):
  command = ' '.join(f"""
    openssl
    enc
    -e
    -{mode}
    -e
    -K {utils.hex_from_bytes(secret)}
    -iv {utils.hex_from_bytes(iv)}
    -nopad
  """.split())
  process = subprocess.run(['bash', '-c', command],
                           input=data,
                           stdout=subprocess.PIPE)
  return process.stdout