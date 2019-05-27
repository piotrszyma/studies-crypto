"""Merkle Hellman knapsack cryptosystem."""

import random
import string

import merkle_hellman_attack as mh_attack

from utils import modinv, gcd


MESSAGE_LEN = 200 # Bits


def gen_priv_key(n):
  knapsack_vector = [
      random.randint(
          (2 ** (i - 1) - 1) * (2 ** n), (2 ** (i - 1) * (2 ** n)))
      for i in range(1, n + 1)]
  modulus = random.randint(2 ** (2 * n + 1) + 1, 2 ** (2 * n + 2) - 1)

  while True:
    try:
      w_inv = random.randint(2, modulus - 2)
      w = modinv(w_inv, modulus)
    except ValueError:
      pass
    else:
      break

  return {
      'a_prim': knapsack_vector,
      'w': w,
      'w_inv': w_inv,
      'modulus': modulus,
      'len': n,
  }

def calculate_pub_key(priv_key):
  a_prim = priv_key['a_prim']
  modulus = priv_key['modulus']
  w = priv_key['w']
  return {
      'a': [(a_prim_i * w) % modulus for a_prim_i in a_prim]
  }

def key_gen(msg_len):
  priv_key = gen_priv_key(msg_len)
  public_key = calculate_pub_key(priv_key)
  return priv_key, public_key

def enc(message, public_key):
  # Message to encode.
  a = public_key['a']
  # Replace x with message
  x = message
  # Encoded to S using a (S is now a "trapdoor knapsack vector").
  S = sum(a_i * x_i for a_i, x_i in zip(a, x))
  return S

def dec(S, priv_key):
  # Message sent to designer, who computes S'.
  w_inv = priv_key['w_inv']
  modulus = priv_key['modulus']
  a_prim = priv_key['a_prim']
  msg_len = priv_key['len']
  S_prim = (w_inv * S) % modulus

  decoded_x = [None for _ in range(msg_len)]

  # Using S_prim and a_prim designer decodes message.
  decoded_x[-1] = 1 if S_prim >= a_prim[-1] else 0

  # from last index - 1 to 0
  for idx in range(msg_len - 2, -1, -1):
    val = S_prim - sum(decoded_x[j] * a_prim[j] for j in range(idx + 1, msg_len))
    decoded_x[idx] = 1 if val >= a_prim[idx] else 0

  return decoded_x

def bits_array_to_bytes(bits_array):
  return (
      int(''.join(map(str, bits_array)), base=2)
      .to_bytes(length=len(bits_array) // 8 + 1, byteorder='big')
  )

def bytes_to_bits_array(bytes_array):
  return list(map(int, bin(int(bytes_array.hex(), base=16))[2:]))


def main():
  # message_bytes = ''.join(random.choices(string.ascii_uppercase, k=5)).encode()
  message_bytes = 'lorem ipsum'.encode()
  message_bits = bytes_to_bits_array(message_bytes)

  priv_key, public_key = key_gen(msg_len=len(message_bits))

  cypher = enc(message_bits, public_key)

  print('Possible solutions found by LLL:')

  for result in mh_attack.mh_attack(public_key['a'], cypher):
    print(result)
    print(bits_array_to_bytes(result))

  print('\n-----')
  decryption_bits = dec(cypher, priv_key)
  decryption_bytes = bits_array_to_bytes(decryption_bits)
  print(decryption_bits)
  print(decryption_bytes)

if __name__ == "__main__":
  main()
