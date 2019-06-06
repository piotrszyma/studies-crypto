import math
import random

def gen_next():
  m = random.randint(25, 256)
  while True:
    a = random.randint(3, m - 1)
    if math.gcd(a, m) == 1:
      break
  print(f'a: {a} m: {m} What is a\u207B\u00B9?')

  while True:
    num = int(input())
    result = num * a % m
    print(f'Results: {result}')
    if result == 1:
      print(
        r"""
      _.-'''''-._
    .'  _     _  '.
   /   (_)   (_)   \
  |  ,           ,  |
  |  \`.       .`/  |
   \  '.`'""'"`.'  /
    '.  `'---'`  .'
      '-._____.-'
        """
      )
      break
    else:
      print('No, try again...')

def main():
  while True:
    gen_next()
    print('Good job! Try next to get better...')

if __name__ == "__main__":
  main()