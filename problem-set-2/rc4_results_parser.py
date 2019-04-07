import glob
import subprocess
import itertools

def tail(file, n):
  proc = subprocess.Popen(['tail', '-n', f'{n}', file], stdout=subprocess.PIPE)
  lines = proc.stdout.readlines()
  return lines


def main():
  outs_files = glob.iglob('test_results/*')
  results = []
  for file in outs_files:
    lines = tail(file, 50)
    found = False
    for line in lines:
      if found:
        results.append(line)
      if b'Summary results' in line:
        found = True
        results.append(line)

  with open('test_sumup.txt', 'wb+') as sumup_file:
    sumup_file.writelines(results)

      # for line in out_file:
      #   print(line)


if __name__ == "__main__":
    main()