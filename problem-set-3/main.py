import argparse
import configparser
import pathlib
import subprocess
import hashlib
import random
import logging
import functools
import sys
import os

from typing import Text

from libs import crypto_libs
from libs import keystore_libs
from libs import utils

MODES_CHOICES = ('aes-128-cbc', 'aes-128-ecb', 'aes-128-ofb')
OPERATION_ENC = 'enc'
OPERATION_DEC = 'dec'
OPERATION_CHOICES = (OPERATION_DEC, OPERATION_ENC)
OUTPUT_STDOUT = object()
PASSWORD_DEFAULT = 'defaultpassword'


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
    return utils.bytes_from_hex(parsed_args.secret)
  print("Type secret (in hex format) to use and press ENTER.")
  return utils.bytes_from_hex(input())


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
    return crypto_libs.decrypt
  elif operation == OPERATION_ENC:
    return crypto_libs.encrypt
  raise AttributeError(f'Unknown operation {operation}')


def get_output(parsed_args):
  if parsed_args.output_path:
    return parsed_args.output_path
  return OUTPUT_STDOUT


def get_config(parsed_args):
  config = configparser.ConfigParser()
  config.read(parsed_args.config_path)
  credentials_config = config['credentials']

  keystore_path = credentials_config.get('keystore')
  password = credentials_config['password']
  if keystore_path:
    privkey = keystore_libs.load_key_from_keystore(keystore_path, password)
    secret = hashlib.sha512(privkey).digest()
  else:
    secret = utils.bytes_from_hex(credentials_config['secret'])
  return secret, password.encode('utf-8')


def get_secret_and_password(parsed_args):
  if parsed_args.config_path:
    secret, password = get_config(parsed_args)
  else:
    secret = get_secret(parsed_args)
    password = get_password(parsed_args)
  return secret, password


def write_output(result, output_target):
  if output_target == OUTPUT_STDOUT:
    os.write(sys.stdout.fileno(), result)
  else:
    pathlib.Path(output_target).write_bytes(result)


def main():
  parsed_args = parse_arguments()
  secret, password = get_secret_and_password(parsed_args)
  data = get_data(parsed_args)
  mode = get_mode(parsed_args)
  operation = get_operation(parsed_args)
  result = operation(data, secret, password, mode)
  output_target = get_output(parsed_args)
  write_output(result, output_target)


if __name__ == "__main__":
  main()
