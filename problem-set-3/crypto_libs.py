import subprocess

from typing import Text

import settings
import utils


def encrypt(data: bytes, secret: bytes, password: bytes, mode: Text) -> bytes:
  assert len(secret) == settings.SECRET_LEN
  command = ' '.join(f"""
    openssl
    enc 
    -e
    -{mode}
    -e
    -K {utils.hex_from_bytes(secret)}
    -k {utils.hex_from_bytes(password)}
    -salt
  """.split())
  process = subprocess.run(['bash', '-c', command],
                           input=data,
                           stdout=subprocess.PIPE)
  return process.stdout


def decrypt(data: bytes, secret: bytes, password: bytes, mode: Text):
  assert len(secret) == settings.SECRET_LEN
  command = ' '.join(f"""
    openssl 
    enc
    -d
    -{mode}
    -K {utils.hex_from_bytes(secret)}
    -k {utils.hex_from_bytes(password)}
    -salt
  """.split())
  process = subprocess.run(['bash', '-c', command],
                           input=data,
                           stdout=subprocess.PIPE)
  return process.stdout
