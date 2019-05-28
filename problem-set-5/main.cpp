#include <iostream>
#include <tuple>
#include <functional>
#include <assert.h>
#include <utility>
#include <fstream>

#include <gmpxx.h>

#include "field.h"


#define ED_CURV_D -11


// Edward curve def
// x_2 + y_2 = 1 + d * x_2 * y_2.

// int modInverse(int a, int m)
// {
//   a = a % m;
//   for (int x=1; x<m; x++) {
//     if ((a*x) % m == 1) {
//       return x;
//     }
//   }
//   return -1;
// }

auto edwardsAdd(std::pair<F, F> left, std::pair<F, F> right) {
  F x1 = left.first;
  F y1 = left.second;
  F x2 = right.first;
  F y2 = right.second;
  F one = left.first.getOne();
  F d = left.first.getD();

  F x3 = (x1 * y2 + y1 * x2) / (one + d * x1 * x2 * y1 * y2);
  F y3 = (y1 * y2 - x1 * x2) / (one - d * x1 * y1 * x2 * y2);
  return std::pair<F, F>(x3, y3);
}

auto scalarMultiply(int n, F_PAIR vector) {
  assert(n >= 0);
  if (n == 0) {
    return F_PAIR(vector.first.getFromModulus(0), vector.first.getFromModulus(1));
  } else if (n == 1) {
    return vector;
  }
  auto multiplied = scalarMultiply(n / 2, vector);
  multiplied = edwardsAdd(multiplied, multiplied);
  if (n % 2) multiplied = edwardsAdd(vector, multiplied);
  return multiplied;
}

auto modulusFactory(mpz_class modulus) {
  return [modulus](mpz_class number) {
    return F(number, modulus);
  };
};


auto modulusFactory(int modulus) {
  mpz_class _modulus = mpz_class(modulus);
  return [_modulus](mpz_class number) {
    return F(number, _modulus);
  };
};

// auto gen() {
//   auto F_1009 = modulusFactory(1009);
//   F_PAIR knownPoint (F_1009(1), F_1009(0)); // P
//   auto privateKey = 581; // a
//   F_PAIR publicKey = scalarMultiply(privateKey, knownPoint); // R
//   return std::make_tuple(knownPoint, publicKey, privateKey); // P, R, a
// }

// auto enc(F message, F_PAIR publicKey, F_PAIR knownPoint) {
//   auto randomKey = 223;
//   auto decPoint = scalarMultiply(randomKey, knownPoint); // Q = k * P
//   auto encPoint = scalarMultiply(randomKey, publicKey); // k * R
//   auto cypher = message * encPoint.first;
//   return std::make_tuple(cypher, decPoint); // (x * m, Q)
// }

// auto dec(F cypher, int privateKey, F_PAIR decPoint) {
//   F_PAIR privDecPoint = scalarMultiply(privateKey, decPoint);
//   F privDecPointX = privDecPoint.first;
//   std::cout << privDecPointX.getValue() << std::endl;
//   auto modInv = modInverse(privDecPointX.getValue(), 1009);
//   std::cout << modInv << std::endl;
// };

int getSeed() {
  unsigned long long int random_value = 0; //Declare value to store data into
  size_t size = sizeof(random_value); //Declare size of data
  std::ifstream urandom("/dev/urandom", std::ios::in|std::ios::binary); //Open stream
  urandom.read(reinterpret_cast<char*>(&random_value), size); //Read from urandom
  return random_value;
}

int main(void) {
  // gmp_randstate_t randomState;
  // gmp_randinit_default(randomState);
  // gmp_randseed_ui(randomState, getSeed());
  // mpz_t randomNumber;
  // mpz_urandomb(randomNumber, randomState, 256);

  // F a = F(mpz_class(randomNumber), mpz_class(randomNumber));

  // std::cout << a.getValue().get_mpz_t() << std::endl;

  // auto F_1009 = modulusFactory(1009);
  // auto genResult = gen();

  // F_PAIR knownPoint = std::get<0>(genResult);
  // F_PAIR publicKey = std::get<1>(genResult);
  // int privateKey = std::get<2>(genResult);

  // F message = F_1009(123);
  // auto encResult = enc(message, publicKey, knownPoint);

  // F cypher = std::get<0>(encResult);
  // F_PAIR decPoint = std::get<1>(encResult);

  // dec(cypher, privateKey, decPoint);


  // ======================================================================
  //
  //                               TESTS
  //
  // ======================================================================

  // For the below tests D value equals -11.
  // auto F_1009 = modulusFactory(1009);
  // assert(ED_CURV_D == -11);
  // assert(F_1009(-1) == F_1009(1008));
  // assert(F_1009(6) != F_1009(5));
  // assert(F_1009(101) + F_1009(1000) == F_1009(92));
  // assert(F_1009(101) - F_1009(1000) == F_1009(110));
  // assert(F_1009(101) * F_1009(1000) == F_1009(100));
  // assert(F_1009(101) * F_1009(112) == F_1009(213));
  // assert(F_1009(101) / F_1009(1000) == F_1009(213));

  // F_PAIR P1 (F_1009(7), F_1009(415));
  // F_PAIR P2 (F_1009(23), F_1009(487));
  // F_PAIR result = edwardsAdd(P1, P2);

  // assert(result.first.getValue() == mpz_class(944));
  // assert(result.second.getValue() == mpz_class(175));

  // F_PAIR multResult = scalarMultiply(5, result);
  // assert(multResult.first.getValue() == 900);
  // assert(multResult.second.getValue() == 799);
  return 0;
};