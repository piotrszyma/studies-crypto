import subprocess
import itertools
import textwrap
import concurrent.futures

def execute_once(n=256, key_len=256, drop=8, mode='n'):
  output_filename = f'test_results/out_{n}_{key_len}_{drop}_{mode}'
  command = (
      './rc4_generator.o'
      f' --n {n}'
      f' --key-len {key_len}'
      f' --drop {drop}'
      f' --mode {mode}'
      f' --test > {output_filename}')
  subprocess.run(['bash', '-c', command])
  with open(output_filename, 'a') as f:
    f.write(textwrap.dedent(f"""
    N: {n}
    Key len: {key_len}
    Drop: {drop}
    Mode: {mode}
    """))


def main():
  N = (16, 64, 256)
  key_len = (40, 64, 128, 256)
  drop = (0, 1, 2, 3)
  mode = ("n", "log")

  with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    for n, k, d, m in itertools.product(N, key_len, drop, mode):
      executor.submit(execute_once, n, k, d, m)

if __name__ == "__main__":
    main()