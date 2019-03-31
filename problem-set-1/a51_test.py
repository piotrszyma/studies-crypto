import unittest

import a51


class A51Tests(unittest.TestCase):
  def test_get_specific_indexes(self):
    lst = [0, 1, 0, 1]
    assert a51.get_specific_indexes(lst, [1, 3]) == [1, 1]
    assert a51.get_specific_indexes(lst, [0]) == [0]
    assert a51.get_specific_indexes(lst, [1, 2]) == [1, 0]

  def test_shift_and_calc_last(self):
    lst = [0, 1, 0, 1, 0, 1]
    assert a51.shift_and_calc_last(lst, [0, 1, 2]) == [*lst[1:], (0 ^ 1 ^ 0)]
    assert a51.shift_and_calc_last(lst, [0, 2]) == [*lst[1:], (0 ^ 0)]
    assert a51.shift_and_calc_last(lst, [0, 2, 5]) == [*lst[1:], (0 ^ 0 ^ 1)]


if __name__ == "__main__":
  unittest.main()
