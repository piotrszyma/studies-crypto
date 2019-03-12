def gcd(a, b):
  while a != 0:
    a, b = b % a, a
  return b


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
  else:
    import pdb
    pdb.set_trace()
    raise ValueError("Unable to calculate modular inverse.")
