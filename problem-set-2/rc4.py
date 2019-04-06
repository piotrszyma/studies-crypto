import argparse
import math
import random

from typing import Generator


def mdrop(PRNG: Generator, D: int) -> int:
  """Applies mdrop on PRNG generator.

  Args:
    PRNG (Generator): generator that creates random values.
    D (int): number of bits to drop.

  Yields:
    int: random numbers.
  """

  while True:
    for _ in range(D):
      next(PRNG)
    yield next(PRNG)


class RC4:
  def __init__(self, key: int):
    self.key = key
    self.L = len(key)
    self.S = None

  def KSA(self, N: int, T: int):
    """Method to generate permutaton.

    Takes a secret key K (self.key) as an input and returns an array
    (permutation S of size N)

    Args:
      N (int): size of array of permutations.
      T (int): number of loop executions while creating permutations.
    """

    S = [i for i in range(N)]
    j = 0
    for i in range(0, T + 1):
      j = (j + S[i % N] + self.key[i % self.L]) % N
      S[i % N], S[j % N] = S[j % N], S[i % N]
    self.S = S

  def PRGA(self, N: int) -> Generator:
    """Generates pseudorandom generator modulo N.

    Args:
      N (int): number to divide modulo by.

    Returns:
      Generator: Pseudorandom generator.
    """

    i = 0
    j = 0
    S = self.S

    while True:
      i = (i + 1) % N
      j = (j + S[i]) % N
      S[i], S[j] = S[j], S[i]
      yield S[(S[i] + S[j]) % N]

def PRGA_32BIT(mdrop_PRGA):
  while True:
    # 2 * 32
    yield (next(mdrop_PRGA) << 16) + (next(mdrop_PRGA) << 8) + next(mdrop_PRGA)

def main():
  T_MODE_N = 'n'
  T_MODE_2NLOGN = 'log'

  T_MODES = {
      T_MODE_N:      lambda N: N,
      T_MODE_2NLOGN: lambda N: 2 * N * math.log(N),
  }

  parser = argparse.ArgumentParser()
  parser.add_argument('-n', type=int, default=256)
  parser.add_argument('--mode', '-m', choices=T_MODES, default=T_MODE_N)
  parser.add_argument('-l', '--key-len', type=int, default=256)
  parser.add_argument('-d', type=int, default=8)
  parser.add_argument('-s', '--size', type=int, default=100)
  parser.add_argument('-f', '--from-file', action='store_true', default=False)
  args = parser.parse_args()

  if args.from_file:
    with open('key.txt', 'r') as f:
      key = [int(n) for n in f.read().split(',')]
  else:
    key = [random.getrandbits(8) for _ in range(args.key_len)]

  N = args.n
  T = int(T_MODES[args.mode](args.n))

  rc4 = RC4(key)
  rc4.KSA(N, T)
  prng = rc4.PRGA(N)

  for num, _ in zip(PRGA_32BIT(mdrop(prng, args.d)), range(args.size)):
    print(num)


if __name__ == "__main__":
  main()