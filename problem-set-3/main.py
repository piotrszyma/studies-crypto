import argparse
import configparser
import pathlib
import subprocess
import random
import logging
import functools
import sys
import os

from typing import Text

STORE_PASS = 'testpass'
STORE_PATH = 'teststore.p12'
SECRET_LEN = 16  # in bytes

MODES_CHOICES = ('aes-128-cbc', )
OPERATION_ENC = 'enc'
OPERATION_DEC = 'dec'
OPERATION_CHOICES = (OPERATION_DEC, OPERATION_ENC)
OUTPUT_STDOUT = object()
PASSWORD_DEFAULT = 'defaultpassword'


def duplets(hex_input: str):
  if len(hex_input) % 2 != 0:
    hex_input = '0' + hex_input
  iterable = iter(hex_input)
  while True:
    yield next(iterable) + next(iterable)


def hex_from_bytes(bytes_input: bytes) -> str:
  return hex(int.from_bytes(bytes_input, byteorder='big'))[2:]


def byte_from_hex(hex_input: str) -> bytes:
  return int(hex_input, base=16).to_bytes(length=1, byteorder='big')


def bytes_from_hex(hex_input: str) -> bytes:
  return functools.reduce(lambda prev, curr: prev + byte_from_hex(curr),
                          duplets(hex_input), b'')


def normalize_secret(secret: bytes):
  return bytes(max(0, SECRET_LEN - len(secret))) + secret[:SECRET_LEN]


def get_key():
  return functools.reduce(lambda prev, curr: prev + curr,
                          (random.getrandbits(8).to_bytes(
                              length=1, byteorder='big')
                           for _ in range(SECRET_LEN)), b'')


def encrypt(data: bytes, secret: bytes, password: bytes, mode: Text) -> bytes:
  assert len(secret) == SECRET_LEN
  command = ' '.join(f"""
    openssl
    enc 
    -e
    -{mode}
    -e
    -K {hex_from_bytes(secret)}
    -k {hex_from_bytes(password)}
    -salt
  """.split())
  process = subprocess.run(['bash', '-c', command],
                           input=data,
                           stdout=subprocess.PIPE)
  return process.stdout


def decrypt(data: bytes, secret: bytes, password: bytes, mode: Text):
  assert len(secret) == SECRET_LEN
  command = ' '.join(f"""
    openssl 
    enc
    -d
    -{mode}
    -K {hex_from_bytes(secret)}
    -k {hex_from_bytes(password)}
    -salt
  """.split())
  process = subprocess.run(['bash', '-c', command],
                           input=data,
                           stdout=subprocess.PIPE)
  return process.stdout


def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      'operation', choices=OPERATION_CHOICES, default=OPERATION_ENC)
  parser.add_argument(
      '--mode',
      '-m',
      choices=MODES_CHOICES,
      help='Mode of encryption to be used.',
      default=MODES_CHOICES[0])
  parser.add_argument('--secret', '-s', type=str, help='Secret in hex format.')
  parser.add_argument('--password', '-p', type=str, default=PASSWORD_DEFAULT)
  parser.add_argument('--input_path', '-i', help="Path to input data.")
  parser.add_argument(
      '--output_path',
      '-o',
      help="Where to store output data.",
      default=OUTPUT_STDOUT)
  parser.add_argument('--config_path', '-c', help='Path to config file.')
  return parser.parse_args()


def get_data(parsed_args) -> bytes:
  if parsed_args.input_path:
    return pathlib.Path(parsed_args.input_path).read_bytes()
  return sys.stdin.buffer.read()


def get_secret(parsed_args) -> bytes:
  if parsed_args.secret:
    return normalize_secret(bytes_from_hex(parsed_args.secret))
  print("Type secret (in hex format) to use and press ENTER.")
  return normalize_secret(bytes_from_hex(input()))


def get_password(parsed_args) -> bytes:
  if parsed_args.password:
    return parsed_args.password.encode('utf-8')
  print("Type password and press ENTER.")
  return sys.stdin.buffer.read()


def get_mode(parsed_args) -> str:
  return parsed_args.mode


def get_operation(parsed_args) -> str:
  operation = parsed_args.operation
  if operation == OPERATION_DEC:
    return decrypt
  elif operation == OPERATION_ENC:
    return encrypt
  else:
    raise AttributeError(f'Unknown operation {operation}')


def get_output(parsed_args):
  if parsed_args.output_path:
    return parsed_args.output_path
  return OUTPUT_STDOUT


def get_config(parsed_args):
  config = configparser.ConfigParser()
  config.read(parsed_args.config_path)
  secret = bytes_from_hex(config['credentials']['secret'])
  password = config['credentials']['password']
  return normalize_secret(secret), password.encode('utf-8')


def main():
  parsed_args = parse_arguments()

  if parsed_args.config_path:
    secret, password = get_config(parsed_args)
  else:
    secret = get_secret(parsed_args)
    password = get_password(parsed_args)
  data = get_data(parsed_args)
  mode = get_mode(parsed_args)
  operation = get_operation(parsed_args)
  result = operation(data, secret, password, mode)
  output_target = get_output(parsed_args)
  if output_target == OUTPUT_STDOUT:
    os.write(1, result)
  else:
    pathlib.Path(output_target).write_bytes(result)


if __name__ == "__main__":
  main()
