#ifndef UTILS_H
#define UTILS_H

#include "field.h"

namespace EcUtils {
  bool isPointOnCurve(FieldNumber x, FieldNumber y);
  int getSeed();
  void printPoint(FieldPoint point);
  void assertPointsEqual(FieldPoint expected, FieldPoint actual);
  FieldPoint getRandomPointOnCurve(mpz_class modulus);
}

#endif //UTILS_H
