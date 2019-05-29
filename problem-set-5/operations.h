#ifndef OPERATIONS_H
#define OPERATIONS_H

#include <gmpxx.h>

#include "field.h"

FieldPoint edwardsAdd(FieldPoint left, FieldPoint right);
FieldPoint scalarMultiply(mpz_class scalar, FieldPoint vector);
FieldPoint scalarMultiply(int n, FieldPoint vector);

mpz_class positiveModulo(mpz_class value, mpz_class modulus);

#endif //OPERATIONS_H