#ifndef OPERATIONS_H
#define OPERATIONS_H

#include <gmpxx.h>

#include "field.h"

namespace EcOperations {
  FieldPoint edwardsAdd(FieldPoint left, FieldPoint right);
  FieldPoint scalarMultiply(mpz_class scalar, FieldPoint vector);
  FieldPoint scalarMultiply(int n, FieldPoint vector);

  mpz_class positiveModulo(mpz_class value, mpz_class modulus);

  mpz_class inverse(mpz_class value, mpz_class modulus);
  FieldNumber xRecover(FieldNumber y);

  // std::function<FieldNumber (mpz_class)> modulusFactory(mpz_class modulus);
  // std::function<FieldNumber (mpz_class)> modulusFactory(int modulus);
}

#endif //OPERATIONS_H