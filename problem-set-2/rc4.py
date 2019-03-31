import array
import random
import sys
import argparse

def get_random(length):
    return


class Bits(list):
  def __init__(self, number):
    super().__init__(self)
    if isinstance(number, int):
      self.extend(bit == '1' for bit in bin(number)[2:])
    elif isinstance(number, list):
      self.extend(number)

  def __repr__(self):
    return '0b' + ''.join(str(int(bit)) for bit in self)

  def __setitem__(self, key, value):
    if isinstance(value, int):
        super().__setitem__(key, bool(value))
    else:
        super().__setitem__(key, value)

  def __getitem__(self, key):
    # Returns i-th bytes
    if isinstance(key, int):
      return int(super().__getitem__(key))
    else:
      return Bits(super().__getitem__(key))

  def __int__(self):
    return self.value()

  def value(self):
    """Returns int value of bits."""
    return int(''.join(str(int(bit)) for bit in self), base=2)

  def byte_slice(self, index):
    return slice(index * 8, (index + 1) * 8)

  def byte(self, index):
    """Returns i-th byte from bits."""
    return self[self.byte_slice(index)]

  def swap(self, left_idx, right_idx):
    self[self.byte_slice(left_idx)], self[self.byte_slice(right_idx)] = (
        self[self.byte_slice(right_idx)], self[self.byte_slice(left_idx)])
    return self


def mdrop(PRNG, D):
  while True:
    for _ in range(D + 1):
      yield next(PRNG)
    for _ in range(D):
      next(PRNG)


class RC4:
  def __init__(self, key):
    self.key = key
    self.L = len(key) // 8
    self.S = None

  def KSA(self, N, T):
    """Method to generate permutaton.

    Takes a secret key K (self.key) as an input and returns an array
    (permutation S of size N)

    Args:
      N - size of permutation to output.

    """
    S = [i for i in range(N)]

    j = 0

    for i in range(0, T + 1):
      j = ( j + S[i % N] + int(self.key[i % self.L])) % N
      S[i % N], S[j % N] = S[j % N], S[i % N]

    self.S = S

  def PRGA(self, N):
    i = 0
    j = 0
    S = self.S

    while True:
      i = (i + 1) % N
      j = (j + S[i]) % N
      S[i], S[j] = S[j], S[i]
      yield S[(S[i] + S[j]) % N]

T_MODE_N = 'n'
T_MODE_2NLOGN = 'log'

T_MODES = {
    T_MODE_N:      lambda N: N,
    T_MODE_2NLOGN: lambda N: 2 * N * math.log(N),
}

parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, default=256)
parser.add_argument('-t', choices=T_MODES, default=T_MODE_N)
parser.add_argument('--key_len', type=int, default=256)
parser.add_argument('-d', type=int, default=8)
parser.add_argument('-s', '--size', type=int, default=100)
args = parser.parse_args()

key = Bits(random.getrandbits(args.key_len))
rc4 = RC4(key)
rc4.KSA(N=args.n, T=T_MODES[args.t](args.n))
prng = rc4.PRGA(args.n)

for num, _ in zip(mdrop(prng, args.d), range(args.size)):
    print(num)
