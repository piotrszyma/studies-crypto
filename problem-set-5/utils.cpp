#include <fstream>
#include <iostream>

#include "utils.h"
#include "field.h"
#include "defines.h"

namespace EcUtils {

  // Edward curve def
  // x_2 + y_2 = 1 + d * x_2 * y_2.
  bool isPointOnCurve(FieldNumber x, FieldNumber y) {
    FieldNumber left = x * x + y * y;
    FieldNumber right = x.getOne() + x.getD() * x * x * y * y;
    return left == right;
  }

  int getSeed() {
    unsigned long long int random_value = 0; //Declare value to store data into
    size_t size = sizeof(random_value); //Declare size of data
    std::ifstream urandom("/dev/urandom", std::ios::in|std::ios::binary); //Open stream
    urandom.read(reinterpret_cast<char*>(&random_value), size); //Read from urandom
    return random_value;
  }

  void printPoint(FieldPoint point) {
    std::cout << "(" << point.first.getValue().get_mpz_t() << ", ";
    std::cout << point.second.getValue().get_mpz_t() << ")" << std::endl;
  }

  FieldPoint getRandomPointOnCurve(mpz_class modulus) {
    gmp_randclass RANDOMNESS (gmp_randinit_default);
    RANDOMNESS.seed(getSeed());
    int ctr;
    mpz_class X(0), Y(0);
    FieldNumber F_X(mpz_class(0), modulus), F_Y(mpz_class(0), modulus);
    for (;;) {
      do {
        X = RANDOMNESS.get_z_range(modulus);
      } while (X == 0);
      F_X = FieldNumber(X, modulus);
      F_Y = FieldNumber(mpz_class(0), modulus);
      ctr = 0;
      do {
        do {
          Y = RANDOMNESS.get_z_range(modulus);
        } while (Y == 0);
        F_Y = FieldNumber(Y, modulus);
        ctr += 1;
        if (ctr == 1000) break;
      } while((!isPointOnCurve(F_X, F_Y)));
      if (ctr < 1000) {
        return {FieldNumber(X, modulus), FieldNumber(Y, modulus)};
      }
    }
  }
}
