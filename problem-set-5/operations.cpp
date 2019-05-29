#include <functional>

#include "field.h"

namespace EcOperations {
  FieldPoint edwardsAdd(FieldPoint left, FieldPoint right) {
    FieldNumber x1 = left.first;
    FieldNumber y1 = left.second;
    FieldNumber x2 = right.first;
    FieldNumber y2 = right.second;
    FieldNumber one = left.first.getOne();
    FieldNumber d = left.first.getD();

    FieldNumber x3 = (x1 * y2 + y1 * x2) / (one + d * x1 * x2 * y1 * y2);
    FieldNumber y3 = (y1 * y2 - x1 * x2) / (one - d * x1 * y1 * x2 * y2);
    return FieldPoint(x3, y3);
  }

  FieldPoint scalarMultiply(mpz_class scalar, FieldPoint vector) {
    if (scalar == 0) {
      return FieldPoint(vector.first.getFromModulus(0), vector.first.getFromModulus(1));
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
      return FieldPoint(vector.first.getFromModulus(0), vector.first.getFromModulus(1));
    } else if (n == 1) {
      return vector;
    }
    auto multiplied = scalarMultiply(n / 2, vector);
    multiplied = edwardsAdd(multiplied, multiplied);
    if (n % 2) multiplied = edwardsAdd(vector, multiplied);
    return multiplied;
  }

  mpz_class positiveModulo(mpz_class value, mpz_class modulus) {
    mpz_class result1, result2, result3;
    mpz_mod(result1.get_mpz_t(), value.get_mpz_t(), modulus.get_mpz_t());
    return result1;
    // return (value % modulus + modulus) % modulus;
  }

  // std::function<FieldNumber (mpz_class)> modulusFactory(mpz_class modulus) {
  //   return [modulus](mpz_class number) {
  //     return FieldNumber(number, modulus);
  //   };
  // };

  // std::function<FieldNumber (mpz_class)> modulusFactory(int modulus) {
  //   mpz_class _modulus = mpz_class(modulus);
  //   return [_modulus](mpz_class number) {
  //     return FieldNumber(number, _modulus);
  //   };
  // };

}
