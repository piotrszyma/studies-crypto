from fractions import Fraction
import math

import numpy as np


# scalar product
def scalar_product(a, b):
  m = len(a)
  res = Fraction(0)
  for i in range(m):
    res += a[i] * b[i]
  return res


# get vector j in the matrix n
def get_vector(n, j):
  return [n[i][j] for i in range(len(n))]


# vector substraction
def vector_add(a, b):
  return [a[i] + b[i] for i in range(len(a))]


# vector substraction
def vector_sub(a, b):
  return [a[i] - b[i] for i in range(len(a))]


# vector multiplication with a constant
def vector_mult_const(v, k):
  return [v[i] * k for i in range(len(v))]


# set the k-th column of matrix n to the vector v
def set_matrix_vector(n, k, v):
  row = len(n)
  for i in range(row):
    n[i][k] = v[i]


# norml2 : square of the L2-norm of the vector x
def norml2(a):
  return scalar_product(a, a)


def round(num):
  if (num > 0):
    return int(num + Fraction(1, 2))
  else:
    return int(num - Fraction(1, 2))


def create_matrix(n):
  row = len(n)
  col = len(n[0])
  res = [[Fraction(n[i][j]) for j in range(col)] for i in range(row)]
  return res


# gram schmidt algorithm
def gram_schmidt(g, m, mu, B):
  col = len(g[0])

  for i in range(col):
    # bi* = bi
    b_i = get_vector(g, i)
    b_i_star = b_i
    set_matrix_vector(m, i, b_i_star)

    for j in range(i):
      # u[i][j] = (bi, bj*)/Bj
      b_j_star = get_vector(m, j)
      b_i = get_vector(g, i)
      B[j] = norml2(b_j_star)
      mu[i][j] = Fraction(scalar_product(b_i, b_j_star), B[j])
      # bi* = bi* - u[i][j]* bj*
      b_i_star = vector_sub(b_i_star, vector_mult_const(b_j_star, mu[i][j]))
      set_matrix_vector(m, i, b_i_star)

    b_i_star = get_vector(m, i)
    # B[i] = (bi*, bi*)
    B[i] = scalar_product(b_i_star, b_i_star)


# reduce
def reduce(g, mu, k, l):
  row = len(g)

  if math.fabs(mu[k][l]) > Fraction(1, 2):
    r = round(mu[k][l])
    b_k = get_vector(g, k)
    b_l = get_vector(g, l)
    # bk = bk - r*bl
    set_matrix_vector(g, k, vector_sub(b_k, vector_mult_const(b_l, r)))

    for j in range(l):
      mu[k][j] = mu[k][j] - r * mu[l][j]

    mu[k][l] = mu[k][l] - r


# lll_reduction from LLL book
def lll_reduction(n, lc=Fraction(3, 4)):
  row = len(n)
  col = len(n[0])

  m = [[Fraction(0) for j in range(col)] for i in range(row)]
  mu = [[Fraction(0) for j in range(col)] for i in range(col)]
  g = [[n[i][j] for j in range(col)] for i in range(row)]
  B = [Fraction(0) for j in range(col)]

  gram_schmidt(g, m, mu, B)

  # k = 2
  k = 1

  while 1:

    # 1 - perform (*) for l = k - 1
    reduce(g, mu, k, k - 1)

    # lovasz condition
    if B[k] < (lc - mu[k][k - 1] * mu[k][k - 1]) * B[k - 1]:
      # 2
      # u = u[k][k-1]
      u = mu[k][k - 1]

      # B = Bk + u^2*Bk-1
      big_B = B[k] + (u * u) * B[k - 1]

      # mu[k][k-1] = u * B[k-1] / B
      mu[k][k - 1] = u * Fraction(B[k - 1], big_B)

      # Bk = Bk-1 * Bk / B
      B[k] = Fraction(B[k - 1] * B[k], big_B)

      # Bk-1 = B
      B[k - 1] = big_B

      # exchange bk and bk-1
      b_k = get_vector(g, k)
      b_k_minus_1 = get_vector(g, k - 1)
      set_matrix_vector(g, k, b_k_minus_1)
      set_matrix_vector(g, k - 1, b_k)

      # for j = 0 .. k-2
      for j in range(k - 1):
        save = mu[k - 1][j]
        mu[k - 1][j] = mu[k][j]
        mu[k][j] = save

      for i in range(k + 1, col):
        save = mu[i][k - 1]
        mu[i][k - 1] = mu[k][k - 1] * mu[i][
            k - 1] + mu[i][k] - u * mu[i][k] * mu[k][k - 1]
        mu[i][k] = save - u * mu[i][k]

      # if k > 2
      if k > 1:
        k = k - 1

    else:
      for l in range(k - 2, -1, -1):
        reduce(g, mu, k, l)

      if k == col - 1:
        return g

      k = k + 1


b = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [82, 123, 287, 83, 248, 373, 10, 471, -548],
]

# out = lll_reduction(b , lc=Fraction(3, 4))

# out = np.array(out)

# for column in out.T:
#   if all(e in (0, 1) for e in column):
#     print(column)

# M[:, 0] - 0 col
# M[0, :] - 0 row


def mh_attack(public_key, message):
  size = len(public_key) + 1
  public_key.append(-message)
  public_key = np.array(public_key)
  arr = np.identity(size, dtype=int)
  arr = arr[:-1, :]
  input = np.vstack((arr, public_key))
  input = [[*row] for row in input]
  out = lll_reduction(input, lc=Fraction(3, 4))
  out = np.array(out)
  for column in out.T:
    column = column[:-1]
    if all(e in (0, 1) for e in column):
      yield list(column)
