import itertools
import random
import textwrap

import rc4

def get_data_header(n, key_len, d, size):
  return textwrap.dedent(f"""
  #==================================================================
  # generator RC4 n: {n} key_len: {key_len} d: {d}
  #==================================================================
  type: d
  count: {size}
  numbit: {int(math.log(n, 2))}
  """)

def main():
  N = (16, 64, 256)
  KEY_LENGTHS = (40, 64, 128)
  D = (0, 1, 2, 3)
  # N = (16,)
  # KEY_LENGTHS = (40,)
  # D = (0,)
  SIZE = 200000

  for n, key_len, d in itertools.product(N, KEY_LENGTHS, D):
    # print(n, key_len, d)
    key = [random.getrandbits(8) for _ in range(key_len)]
    scheme = rc4.RC4(key)
    scheme.KSA(n, n)
    PRNG = rc4.mdrop(scheme.PRGA(n), d)
    just = len(str(n))

    with open(f'test_data/{n}_{key_len}_{d}_outputs.txt', 'w') as f:
      f.write(get_data_header(n, key_len, d, SIZE))
      for n, _ in zip(PRNG, range(SIZE)):
        f.write(f'{str(n).rjust(just)}\n')

if __name__ == "__main__":
    main()