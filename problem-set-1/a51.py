import functools
import operator
import random


def get_specific_indexes(iterable, indexes):
  return [
      value for index, value in enumerate(iterable)
      if index in frozenset(indexes)
  ]


def shift_and_calc_last(iterable, xored_indexes):
  return [
      *iterable[1:],
      functools.reduce(operator.xor,
                       get_specific_indexes(iterable, xored_indexes))
  ]


class A51:
  def __init__(self, seed):
    assert len(seed) == 23
    self.lsfr1 = seed[:19]
    self.lsfr2 = seed[:22]
    self.lsfr3 = seed[:23]

  def shift_lsfrs(self):
    self.lsfr1 = shift_and_calc_last(self.lsfr1, [18, 17, 16, 13])
    self.lsfr2 = shift_and_calc_last(self.lsfr2, [21, 20])
    self.lsfr3 = shift_and_calc_last(self.lsfr3, [22, 21, 20, 7])

  def calc_random(self):
    return self.lsfr1[0] ^ self.lsfr2[0] ^ self.lsfr3[0]

  def __iter__(self):
    return self

  def __next__(self):
    self.shift_lsfrs()
    return self.calc_random()


def main():
  # seed = [random.randrange(0, 2) for _ in range(23)]
  seed = [int(bit) for bit in '00011111110111110010100']
  a51 = A51(seed)
  for random_number in a51:
    print(random_number)


if __name__ == "__main__":
  main()
