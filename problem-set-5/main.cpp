#include <iostream>
#include <tuple>
#include <functional>
#include <assert.h>
#include <utility>

#include <gmpxx.h>

#include "defines.h"
#include "field.h"
#include "operations.h"
#include "utils.h"


// Edward curve def
// x_2 + y_2 = 1 + d * x_2 * y_2.

mpz_class getNextPrime(mpz_class n) {
  mpz_t tmp;
  mpz_init(tmp);
  mpz_nextprime(tmp, n.get_mpz_t());
  mpz_class tmp_class(tmp);
  mpz_clear(tmp);
  return tmp_class;
}


void performEncryptionProcess() {
  gmp_randclass RANDOMNESS (gmp_randinit_default);
  RANDOMNESS.seed(EcUtils::getSeed());
  mpz_class modulus = getNextPrime(RANDOMNESS.get_z_bits(10));

  std::cout << "Modulus: " << modulus.get_mpz_t() << std::endl;

  // ================== GEN ==================
  // 1. Generate point P.
  FieldPoint P_point = EcUtils::getRandomPointOnCurve(modulus);

  // 2. Generate private key a.
  mpz_class a_number = RANDOMNESS.get_z_range(modulus);

  // 3. Generate public key. (R = aP)
  FieldPoint R_point = EcOperations::scalarMultiply(a_number, P_point);

  // ================== ENC ==================

  // 1. Generate random k.
  mpz_class k_number = RANDOMNESS.get_z_range(modulus);

  // 2. Generate point Q. (Q = k * P)
  FieldPoint Q_point = EcOperations::scalarMultiply(k_number, P_point);

  // 3. Generate 'encryption point'. (kR = k * R)
  FieldPoint kR_point = EcOperations::scalarMultiply(k_number, R_point);

  // 4. Generate message. (point on curve)
  FieldPoint message = EcUtils::getRandomPointOnCurve(modulus);
  EcUtils::printPoint(message);

  // 5. Encrypt message using x from kR = k * R = k * a * P.
  FieldPoint cypher = EcOperations::edwardsAdd(message, kR_point);

  // ================== DEC ==================

  // 1. Get x using private key a and point Q. (aQ = a * Q = a * k * P)
  FieldPoint aQ_point = EcOperations::scalarMultiply(a_number, Q_point);

  // 2. Get aQ inverse. (aQ = k * a * P)
  FieldPoint dec_aQ_point = FieldPoint(-aQ_point.first, aQ_point.second);

  // 3. Decypher message.
  FieldPoint dec_message = EcOperations::edwardsAdd(dec_aQ_point, cypher);

  EcUtils::printPoint(dec_message);
}


// void performTesting() {
//   // For the below tests D value equals -11.
//   auto F_1009 = EcOperations::modulusFactory(1009);
//   assert(EcDefines::EDWARDS_CURVE_D_PARAM == -11);
//   assert(F_1009(-1) == F_1009(1008));
//   assert(F_1009(6) != F_1009(5));
//   assert(F_1009(101) + F_1009(1000) == F_1009(92));
//   assert(F_1009(101) - F_1009(1000) == F_1009(110));
//   assert(F_1009(101) * F_1009(1000) == F_1009(100));
//   assert(F_1009(101) * F_1009(112) == F_1009(213));
//   assert(F_1009(101) / F_1009(1000) == F_1009(213));

//   FieldPoint P1 (F_1009(7), F_1009(415));
//   FieldPoint P2 (F_1009(23), F_1009(487));
//   FieldPoint result = EcOperations::edwardsAdd(P1, P2);

//   assert(result.first.getValue() == mpz_class(944));
//   assert(result.second.getValue() == mpz_class(175));

//   FieldPoint multResult = EcOperations::scalarMultiply(5, result);
//   assert(multResult.first.getValue() == 900);
//   assert(multResult.second.getValue() == 799);
// }


int main(void) {
  performEncryptionProcess();

  return 0;
};