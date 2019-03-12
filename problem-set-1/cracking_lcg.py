import functools
import itertools
import subprocess

import utils


class LCG:
  multiplier = 1103515245
  increment = 12345
  modulus = 2**31

  # multiplier = 672257317069504227
  # increment = 7382843889490547368
  # modulus = 9223372036854775783

  def __init__(self, seed):
    self.state = seed

  def __iter__(self):
    return self

  def __next__(self):
    self.state = (self.state * self.multiplier + self.increment) % self.modulus
    return self.state


def solve_with_unknown_increment(multiplier, modulus, samples):
  increment = (samples[1] - samples[0] * multiplier) % modulus
  return increment


def solve_with_unknown_increment_and_multiplier(modulus, samples):
  multiplier = (((samples[2] - samples[1]) % modulus) * utils.modinv(
      (samples[1] - samples[0]) % modulus, modulus)) % modulus
  increment = solve_with_unknown_increment(multiplier, modulus, samples)
  return multiplier, increment


def solve_with_all_unknown(samples):
  diffs = [s1 - s0 for s0, s1 in zip(samples, samples[1:])]
  modular_zeros = [
      t2 * t0 - t1 * t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])
  ]
  modulus = abs(functools.reduce(utils.gcd, modular_zeros))
  multiplier, increment = solve_with_unknown_increment_and_multiplier(
      modulus, samples)
  return modulus, multiplier, increment


def zip_many(iterable, size):
  return zip(*(tuple(iterable)[idx:] for idx in range(size)))


def _get_glibc_output(size, seed=1):
  proc = subprocess.Popen(
      ['./glibc_random', str(size), str(seed)], stdout=subprocess.PIPE)
  out, _ = proc.communicate()
  return [int(num) for num in out.decode('utf-8').split('\n') if num]


def cracking_custom_lcg():
  number_generator = LCG(123)
  for sample_set in zip_many(itertools.islice(number_generator, 0, 1000), 32):
    modulus, multiplier, increment = solve_with_all_unknown(sample_set)
    assert increment == LCG.increment
    assert multiplier == LCG.multiplier
    assert modulus == LCG.modulus


def cracking_glibc_random():
  samples = _get_glibc_output(30)
  for sample_set in zip_many(samples, 10):
    modulus, multiplier, increment = solve_with_all_unknown(sample_set)
    assert increment == LCG.increment
    assert multiplier == LCG.multiplier
    assert modulus == LCG.modulus


def main():
  cracking_glibc_random()


if __name__ == "__main__":
  main()
