import math
import numpy as np

# M[:, 0] - 0 col
# M[0, :] - 0 row


def GS(matrix):
  n = matrix.shape[0] - 1
  X = matrix.copy()
  X.fill(0)
  Y = matrix.copy()
  Y.fill(0)
  X[:, 0] = matrix[:, 0]
  for j in range(1, n + 1):  # 1, ..., n
    X[:, j] = matrix[:, j]
    for i in range(0, j):  # 0, ..., j - 1
      dot_prod = X[:, i] @ matrix[:, j]
      norm = np.linalg.norm(X[:, i])**2
      Y[i][j] = dot_prod / norm
      X[j] = X[j] - Y[i][j] * X[i]
  return X, Y


# M[:, 0] - 0 col
# M[0, :] - 0 row


def LLL(matrix):
  while True:
    n = matrix.shape[0] - 1
    X, Y = GS(matrix)
    for j in range(1, n + 1):  # 1, ..., n
      for i in range(j - 1, -1, -1):  # j-1, ..., 0
        if Y[i][j] > 0.5:
          matrix[:, j] = matrix[:, j] - math.floor(Y[i][j] +
                                                   0.5) * matrix[:, i]
    X, Y = GS(matrix)

    for j in range(n):  # 0, ..., n-1
      if (np.linalg.norm(X[:, j + 1] + Y[j][j + 1] * X[:, j])**2 <
          0.75 * np.linalg.norm(X[:, j])**2):
        matrix[:, j], matrix[:, j + 1] = matrix[:, j + 1], matrix[:, j]
        break
    else:
      return matrix


S = np.array([2, 3, 7, 14, 30, 57, 120, 251])  # Private key.
n = 491  # modulus
m = 41  # num
m_inv = 12  # num inverse

T = np.array([s * m % n for s in S])  # Public key.

# Message
msg = np.array([1, 0, 0, 1, 0, 1, 1, 0])

cypher = sum(value * weight for value, weight in zip(T, msg))

M_last = np.append(T, -cypher)

M_identity = np.identity(9, dtype=int)[:][:-1]  # size(M) + 1 = 9
M = np.vstack((M_identity, M_last))

print(M)

print('[', end='')
for row in M:
  print('[', end='')
  for cell in row:
    print(cell, ', ', end='')
  print('],')
print(']')
# result = LLL(M)

# import pdb
# pdb.set_trace()
