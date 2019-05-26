import sys
num = ''.join(sys.argv[1].split(':'))
print(int(num, base=16))