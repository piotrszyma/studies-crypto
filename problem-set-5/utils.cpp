#include <fstream>
#include <iostream>

#include "utils.h"
#include "field.h"
#include "operations.h"

namespace EcUtils {

  // Edward curve def
  // x_2 + y_2 = 1 + d * x_2 * y_2.
  bool isPointOnCurve(FieldNumber x, FieldNumber y) {
    FieldNumber left = x * x + y * y;
    FieldNumber right = x.getN(1) + x.getD() * x * x * y * y;
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
    std::cout << "X: " << point.first.getValue().get_mpz_t() << std::endl;
    std::cout << "Y: " << point.second.getValue().get_mpz_t() << std::endl << std::endl;
  }


  void assertPointsEqual(FieldPoint expected, FieldPoint actual) {
    assert(expected.first == actual.first);
    assert(expected.second == actual.second);
  }

  FieldPoint getRandomPointOnCurve(mpz_class modulus) {
    gmp_randclass RANDOMNESS (gmp_randinit_default);
    RANDOMNESS.seed(getSeed());
    mpz_class X(0), Y(0);
    FieldNumber F_Y;
    FieldNumber F_X;

    do {
      mpz_class random = RANDOMNESS.get_z_range(FieldNumber::MODULUS);
      F_Y = FieldNumber(random);
      F_X = EcOperations::xRecover(F_Y);
    } while(!isPointOnCurve(F_X, F_Y));

    return FieldPoint(F_X, F_Y);
  }
}
