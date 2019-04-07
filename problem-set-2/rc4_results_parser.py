import glob
import subprocess
import itertools
import re
import csv


def tail(file, n):
  proc = subprocess.Popen(['tail', '-n', f'{n}', file], stdout=subprocess.PIPE)
  lines = proc.stdout.readlines()
  return lines


def main():
  outs_files_paths = glob.iglob('test_results/*')
  results = []
  for file_path in outs_files_paths:
    # with open(file_path, 'r') as textfile:
    lines = tail(file_path, 50)
    str_lines = []
    for line in lines:
      try:
        str_lines.append(line.decode('utf-8'))
      except UnicodeDecodeError:
        pass
    filetext = ''.join(str_lines)
    # filetext = ''.join(line.decode('utf-8') for line in tail(file_path, 50))
    matches = re.findall("SmallCrush[^^]*(-){46}(?P<results>[^^]*)(-){46}", filetext)
    try:
      failed = sum( 1 for _ in (r.strip() for r in matches[0][1].split('\n') if r.strip()))
    except IndexError:
      failed = 0
    # out_{n}_{key_len}_{drop}_{mode}
    n, key_len, drop, mode = file_path.split('_')[2:]
    n = int(n)
    key_len = int(key_len)
    drop = int(drop)
    mode = mode.split('.')[0]
    results.append((n, key_len, drop, mode, failed))

  results = sorted(results, key=lambda t: t[:-1])
  with open('out.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(results)
    # results.append((, failed))
    # results = sorted(results, key=lambda e: e[0])
    # lines = tail(file, 50)
    # found = False
    # for line in lines:
    #   if found:
    #     results.append(line)
    #   if b'Summary results' in line:
    #     found = True
    #     results.append(line)

  # with open('test_sumup.txt', 'wb+') as sumup_file:
  #   sumup_file.writelines(results)

      # for line in out_file:
      #   print(line)


if __name__ == "__main__":
    main()