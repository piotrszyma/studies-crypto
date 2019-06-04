import tempfile
import subprocess


def xgcd(a, b):
  """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
  x0, x1, y0, y1 = 0, 1, 1, 0
  while a != 0:
    q, b, a = b // a, a, b % a
    y0, y1 = y1, y0 - q * y1
    x0, x1 = x1, x0 - q * x1
  return b, x0, y0


def modinv(num, modular):
  g, x, _ = xgcd(num, modular)
  if g == 1:
    return x % modular
  raise ValueError("Unable to calculate modular inverse.")

# 1385409854850246784644682622624349784560468558795524903 1524938362073628791222322453937223798227099080053904149
def main():
  p = 1385409854850246784644682622624349784560468558795524903
  q = 1524938362073628791222322453937223798227099080053904149
  n = p * q
  e = 65537
  # d = 23
  d = modinv(e, (p - 1) * (q - 1))
  # assert d == modinv(e, (p - 1) * (q - 1))
  e1 = d % (p - 1)
  e2 = d % (q - 1)
  coeff = modinv(q, p)

  data = (
f"""asn1=SEQUENCE:rsa_key

[rsa_key]
version=INTEGER:0
modulus=INTEGER:{n}
pubExp=INTEGER:{e}
privExp=INTEGER:{d}
p=INTEGER:{p}
q=INTEGER:{q}
e1=INTEGER:{e1}
e2=INTEGER:{e2}
coeff=INTEGER:{coeff}""")
  with tempfile.NamedTemporaryFile() as f:
    f.write(data.encode())
    f.flush()
    subprocess.run(
      ['bash', '-c', f'openssl asn1parse -genconf {f.name} -out newkey.der -noout'],
      stderr=subprocess.PIPE)
    result = subprocess.run(
      ['bash', '-c', 'openssl rsa -in newkey.der -inform der'],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
    )
    print(result.stdout.decode(), end='')
    subprocess.run(
      ['bash', '-c', 'rm newkey.der']
    )

if __name__ == "__main__":
  main()
