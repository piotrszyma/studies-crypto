#include <functional>

#include "field.h"

namespace EcOperations {
  FieldPoint edwardsAdd(FieldPoint left, FieldPoint right) {
    FieldNumber x1 = left.first;
    FieldNumber y1 = left.second;
    FieldNumber x2 = right.first;
    FieldNumber y2 = right.second;
    FieldNumber one = left.first.getN(1);
    FieldNumber d = left.first.getD();

    FieldNumber x3 = (x1 * y2 + y1 * x2) / (one + d * x1 * x2 * y1 * y2);
    FieldNumber y3 = (y1 * y2 - x1 * x2) / (one - d * x1 * y1 * x2 * y2);
    return FieldPoint(x3, y3);
  }

  FieldPoint scalarMultiply(mpz_class scalar, FieldPoint vector) {
    if (scalar == 0) {
      return FieldPoint(vector.first.getN(0), vector.first.getN(1));
    } else if (scalar == 1) {
      return vector;
    }
    auto multiplied = scalarMultiply(scalar / 2, vector);
    multiplied = edwardsAdd(multiplied, multiplied);
    if ((scalar & 1) == 1) multiplied = edwardsAdd(vector, multiplied);
    return multiplied;
  }

  FieldPoint scalarMultiply(int n, FieldPoint vector) {
    assert(n >= 0);
    if (n == 0) {
      return FieldPoint(vector.first.getN(0), vector.first.getN(1));
    } else if (n == 1) {
      return vector;
    }
    auto multiplied = scalarMultiply(n / 2, vector);
    multiplied = edwardsAdd(multiplied, multiplied);
    if (n % 2) multiplied = edwardsAdd(vector, multiplied);
    return multiplied;
  }

  mpz_class positiveModulo(mpz_class value, mpz_class modulus) {
    mpz_class result;
    mpz_mod(result.get_mpz_t(), value.get_mpz_t(), modulus.get_mpz_t());
    return result;
    // return (value % modulus + modulus) % modulus;
  }

  mpz_class expmod(mpz_class b, mpz_class e, mpz_class m) {
    mpz_class result;
    mpz_powm(result.get_mpz_t(), b.get_mpz_t(), e.get_mpz_t(), m.get_mpz_t());
    return result;
  }

  mpz_class inverse(mpz_class value, mpz_class modulus) {
    mpz_class result;
    mpz_invert(result.get_mpz_t(), value.get_mpz_t(), modulus.get_mpz_t());
    return result;
  }

  FieldNumber xRecover(FieldNumber y) {
    // Setup I
    mpz_class iVal;
    mpz_class iExp = (y.getModulus() - 1) / 4;
    mpz_powm(iVal.get_mpz_t(), mpz_class(2).get_mpz_t(), iExp.get_mpz_t(), y.getModulus().get_mpz_t());
    FieldNumber I = y.getN(iVal);
    // End setup I

    FieldNumber xx = (y * y - y.getN(1)) / (y.getD() * y * y - y.getN(1));

    mpz_class exponent = (y.getModulus() + 3) / 8;
    mpz_class xVal;
    mpz_powm(xVal.get_mpz_t(), xx.getValue().get_mpz_t(), exponent.get_mpz_t(), y.getModulus().get_mpz_t());

    FieldNumber x = y.getN(xVal);

    if ((x * x - xx) != y.getN(0)) {
      x = x * I;
    }

    if (x % y.getN(2) != y.getN(0)) {
      x = x.getN(x.getModulus()) - x;
    }

    return x;
  }
}
