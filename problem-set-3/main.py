import argparse
import configparser
import pathlib
import hashlib
import sys
import random
import os
import functools

from typing import Text

from libs import crypto_libs
from libs import keystore_libs
from libs import utils

MODES_CHOICES = ('aes-128-cbc', 'aes-128-ecb', 'aes-128-ofb')
OPERATION_ENC = 'enc'
OPERATION_DEC = 'dec'
OPERATION_SEC_ENC = 'sec-enc'
OPERATION_SEC_DEC = 'sec-dec'
OPERATION_CHOICES = (OPERATION_DEC, OPERATION_ENC, OPERATION_SEC_ENC, OPERATION_SEC_DEC)
OUTPUT_STDOUT = object()
PASSWORD_DEFAULT = 'defaultpassword'

def get_inc_iv():
  prev_iv_path = pathlib.Path('/tmp/prev_iv_path')
  if prev_iv_path.exists():
    previous_iv = prev_iv_path.read_bytes()
    random_iv = utils.increment_bytes(previous_iv)
  else:
    random_iv = utils.random_bytes(16)
  prev_iv_path.write_bytes(random_iv)
  return random_iv

def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('--challenge', action='store_true')
  parser.add_argument('--increment_iv', action='store_true')
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
  parser.add_argument('--input_folder', help="Path to input data folder.")
  parser.add_argument('--output_folder', help="Name of output data folder.")
  parser.add_argument('--config_path', '-c', help='Path to config file.')
  return parser.parse_args()


def get_data(parsed_args) -> bytes:
  if parsed_args.input_path:
    return pathlib.Path(parsed_args.input_path).read_bytes()
  return sys.stdin.buffer.read()


def get_secret(parsed_args) -> bytes:
  if parsed_args.config_path:
    config = configparser.ConfigParser()
    config.read(parsed_args.config_path)
    credentials_config = config['credentials']
    keystore_path = credentials_config.get('keystore')
    password = credentials_config['password']
    privkey = keystore_libs.load_key_from_keystore(keystore_path, password)
    return hashlib.sha512(privkey).digest()
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

def write_output(result, output_target):
  if output_target == OUTPUT_STDOUT:
    os.write(sys.stdout.fileno(), result)
  else:
    pathlib.Path(output_target).write_bytes(result)


def main():
  parsed_args = parse_arguments()
  secret = get_secret(parsed_args)
  mode = get_mode(parsed_args)
  operation = get_operation(parsed_args)

  if parsed_args.increment_iv and parsed_args.operation == OPERATION_ENC:
    operation = functools.partial(operation, iv=get_inc_iv())

  if not parsed_args.input_folder:
    data = get_data(parsed_args)
    result = operation(data, secret, mode)
    output_target = get_output(parsed_args)
    write_output(result, output_target)
    return

  input_folder = pathlib.Path(parsed_args.input_folder)

  if parsed_args.challenge:
    data_file = random.choice([
        file_name for file_name in input_folder.iterdir() if file_name.is_file()])
    data = data_file.read_bytes()
    result = operation(data, secret, mode)
    output_target = get_output(parsed_args)
    write_output(result, output_target)
    return

  output_folder = pathlib.Path(
      input_folder.parent, parsed_args.output_folder)
  output_folder.mkdir()

  for file_name in (
        file_name for file_name in input_folder.iterdir() if file_name.is_file()):
    input_data = file_name.read_bytes()
    output_data = operation(input_data, secret, mode)
    pathlib.Path(output_folder, file_name.name).write_bytes(output_data)



if __name__ == "__main__":
  main()
