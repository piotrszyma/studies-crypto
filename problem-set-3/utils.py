import functools

import settings


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
  return bytes(max(
      0, settings.SECRET_LEN - len(secret))) + secret[:settings.SECRET_LEN]
