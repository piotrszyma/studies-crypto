import functools
import itertools
import subprocess

import utils

CONST_2_32 = 2**32


class LCG:
  multiplier = 1103515245
  increment = 12345
  modulus = 2**31

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


def verify(outputs, index, s, s_3, s_31):
  index = -(index + 1)
  x_31 = (outputs[index - 31] << 1) + s_31
  x_3 = (outputs[index - 3] << 1) + s_3
  x = (outputs[index] << 1) + s
  return (x_31 + x_3) % CONST_2_32 == x % CONST_2_32


POSSIBLE_TRIPLETS = ((0, 1, 1), (1, 0, 1), (0, 0, 0), (1, 1, 0))


def glibc_predictor(outputs):
  cases = [([], 0)]
  results = None
  max_index = len(outputs) - 33 + 1
  while cases:
    case = cases.pop()
    shifts, index = case

    if index == max_index:
      result = shifts[:max_index][::-1]
      last_outputs = outputs[-max_index:]
      random_seed = [(out << 1) + shift
                     for out, shift in zip(last_outputs, result)]
      results = random_seed
      continue

    for s, s_3, s_31 in POSSIBLE_TRIPLETS:
      new_shifts = shifts.copy()

      if not verify(outputs, index, s, s_3, s_31):
        continue

      no_lack = (index + 31) - len(new_shifts) + 1
      if no_lack > 0:
        new_shifts.extend((None for _ in range(no_lack)))

      if new_shifts[index] is not None and new_shifts[index] != s:
        continue
      new_shifts[index] = s
      if new_shifts[index + 3] is not None and new_shifts[index + 3] != s_3:
        continue
      new_shifts[index + 3] = s_3
      if new_shifts[index + 31] is not None and new_shifts[index + 31] != s_31:
        continue
      new_shifts[index + 31] = s_31

      cases.append((new_shifts, index + 1))

  results = results[-31:]

  while True:
    results.append((results[-3] + results[-31]) % CONST_2_32)
    results.pop(0)
    yield results[-1] >> 1


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
  for seed in (1, 1232, 123, 5):
    glibc_randoms = _get_glibc_output(52500, seed=seed)
    # PRED_SIZE = 100
    for pred_size in range(88, 123):
      for_predictor = glibc_randoms[:pred_size]
      to_compare = glibc_randoms[pred_size:]
      for original, predicted in zip(to_compare,
                                     glibc_predictor(for_predictor)):
        try:
          assert original == predicted
        except AssertionError:
          print(f'Failed (seed: {seed}) for {pred_size}')
          break
      else:
        print(f'Success (seed: {seed}) for {pred_size}')


def main():
  cracking_glibc_random()


if __name__ == "__main__":
  main()
