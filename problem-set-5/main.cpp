#include <iostream>
#include <tuple>
#include <functional>
#include <assert.h>
#include <utility>
#include <fstream>

#include <gmpxx.h>

#include "field.h"


#define ED_CURV_D -11

gmp_randclass RANDOMNESS (gmp_randinit_default);


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

auto scalarMultiply(mpz_class scalar, F_PAIR vector) {
  if (scalar == 0) {
    return F_PAIR(vector.first.getFromModulus(0), vector.first.getFromModulus(1));
  } else if (scalar == 1) {
    return vector;
  }
  auto multiplied = scalarMultiply(scalar / 2, vector);
  multiplied = edwardsAdd(multiplied, multiplied);
  if ((scalar & 1) == 1) multiplied = edwardsAdd(vector, multiplied);
  return multiplied;
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

mpz_class getNextPrime(mpz_class n) {
  mpz_t tmp;
  mpz_init(tmp);
  mpz_nextprime(tmp, n.get_mpz_t());
  mpz_class tmp_class(tmp);
  mpz_clear(tmp);
  return tmp_class;
}

int getSeed() {
  unsigned long long int random_value = 0; //Declare value to store data into
  size_t size = sizeof(random_value); //Declare size of data
  std::ifstream urandom("/dev/urandom", std::ios::in|std::ios::binary); //Open stream
  urandom.read(reinterpret_cast<char*>(&random_value), size); //Read from urandom
  return random_value;
}

// Edward curve def
// x_2 + y_2 = 1 + d * x_2 * y_2.
bool isPointOnCurve(F x, F y) {
  F left = x * x + y * y;
  F right = x.getOne() + x.getD() * x * x * y * y;
  return left == right;
}

F_PAIR getRandomPointOnCurve(mpz_class modulus) {
  int ctr;
  mpz_class X(0), Y(0);
  F F_X(MPZ_ZERO, modulus), F_Y(MPZ_ZERO, modulus);
  for (;;) {
    do {
      X = RANDOMNESS.get_z_range(modulus);
    } while (X == 0);
    F_X = F(X, modulus);
    F_Y = F(MPZ_ZERO, modulus);
    ctr = 0;
    do {
      do {
        Y = RANDOMNESS.get_z_range(modulus);
      } while (Y == 0);
      F_Y = F(Y, modulus);
      ctr += 1;
      if (ctr == 1000) break;
    } while((!isPointOnCurve(F_X, F_Y)));
    if (ctr < 1000) {
      return {F(X, modulus), F(Y, modulus)};
    }
  }
}

void printPoint(F_PAIR point) {
   std::cout << "(" << point.first.getValue().get_mpz_t() << ", ";
   std::cout << point.second.getValue().get_mpz_t() << ")" << std::endl;
}

void performEncryption() {
  RANDOMNESS.seed(getSeed());
  mpz_class modulus = getNextPrime(RANDOMNESS.get_z_bits(10));

  std::cout << "Modulus: " << modulus.get_mpz_t() << std::endl;

  // ================== GEN ==================
  // 1. Generate point P.
  F_PAIR P_point = getRandomPointOnCurve(modulus);

  // 2. Generate private key a.
  mpz_class a_number = RANDOMNESS.get_z_range(modulus);

  // 3. Generate public key. (R = aP)
  F_PAIR R_point = scalarMultiply(a_number, P_point);

  // ================== ENC ==================

  // 1. Generate random k.
  mpz_class k_number = RANDOMNESS.get_z_range(modulus);

  // 2. Generate point Q. (Q = k * P)
  F_PAIR Q_point = scalarMultiply(k_number, P_point);

  // 3. Generate 'encryption point'. (kR = k * R)
  F_PAIR kR_point = scalarMultiply(k_number, R_point);

  // 4. Generate message. (point on curve)
  F_PAIR message = getRandomPointOnCurve(modulus);
  printPoint(message);

  // 5. Encrypt message using x from kR = k * R = k * a * P.
  F_PAIR cypher = edwardsAdd(message, kR_point);

  // ================== DEC ==================

  // 1. Get x using private key a and point Q. (aQ = a * Q = a * k * P)
  F_PAIR aQ_point = scalarMultiply(a_number, Q_point);

  // 2. Get aQ inverse. (aQ = k * a * P)
  F_PAIR dec_aQ_point = F_PAIR(-aQ_point.first, aQ_point.second);

  // 3. Decypher message.
  F_PAIR dec_message = edwardsAdd(dec_aQ_point, cypher);

  printPoint(dec_message);
}


int main(void) {
  // for(int i =0;i<100;i++) {
  performEncryption();
  // }

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