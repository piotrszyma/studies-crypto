#ifndef UTILS_H
#define UTILS_H

#include "field.h"

namespace EcUtils {
  // extern gmp_randclass RANDOMNESS (gmp_randinit_default);

  bool isPointOnCurve(FieldNumber x, FieldNumber y);
  int getSeed();
  void printPoint(FieldPoint point);
  FieldPoint getRandomPointOnCurve(mpz_class modulus);
}

#endif //UTILS_H
