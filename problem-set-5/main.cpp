#include <iostream>
#include <tuple>
#include <functional>
#include <assert.h>
#include <utility>

#include <gmpxx.h>

#include "field.h"
#include "operations.h"
#include "utils.h"


// Edward curve def
// x_2 + y_2 = 1 + d * x_2 * y_2.
mpz_class MODULUS;
mpz_class D_VALUE;
mpz_class I_VALUE;

void setupConsts() {
  // Modulo.
  mpz_ui_pow_ui(MODULUS.get_mpz_t(), 2, 255);
  mpz_sub_ui(MODULUS.get_mpz_t(), MODULUS.get_mpz_t(), 19);

  // D.
  D_VALUE = -121665;
  mpz_class divisor = 121666;
  mpz_invert(divisor.get_mpz_t(), divisor.get_mpz_t(), MODULUS.get_mpz_t());
  D_VALUE *= divisor;

  // I.
  mpz_class two = 2;
  mpz_class exponent(MODULUS);
  exponent = (exponent - 1) / 4;
  mpz_powm(I_VALUE.get_mpz_t(), mpz_class(2).get_mpz_t(), exponent.get_mpz_t(), MODULUS.get_mpz_t());

  FieldNumber::D_VALUE = D_VALUE;
  FieldNumber::I_VALUE = I_VALUE;
  FieldNumber::MODULUS = MODULUS;
}

FieldPoint generateGenerator() {
  FieldNumber y = FieldNumber(4) / FieldNumber(5);
  FieldNumber x = EcOperations::xRecover(y);
  return FieldPoint(x, y);
}

void performEncryptionProcess() {

  gmp_randclass RANDOMNESS (gmp_randinit_default);
  RANDOMNESS.seed(EcUtils::getSeed());

  // ================== GEN ==================
  // 1. Get point P.
  FieldPoint P = generateGenerator();
  assert(EcUtils::isPointOnCurve(P.first, P.second));

  // 2. Generate private key a.
  mpz_class a = RANDOMNESS.get_z_range(FieldNumber::MODULUS);

  // 3. Generate public key. (R = aP)
  FieldPoint R_point = EcOperations::scalarMultiply(a, P);

  // ================== ENC ==================

  // 1. Generate random k.
  mpz_class k = RANDOMNESS.get_z_range(FieldNumber::MODULUS);

  // 2. Generate point Q. (Q = k * P)
  FieldPoint Q = EcOperations::scalarMultiply(k, P);

  // 3. Generate 'encryption point'. (kR = k * R)
  FieldPoint kR = EcOperations::scalarMultiply(k, R_point);

  // 4. Generate message. (point on curve)
  FieldPoint message = EcUtils::getRandomPointOnCurve(FieldNumber::MODULUS);
  std::cout << "Message:" << std::endl;
  EcUtils::printPoint(message);

  // 5. Encrypt message using x from kR = k * R = k * a * P.
  FieldPoint cypher = EcOperations::edwardsAdd(message, kR);
  std::cout << "Cypher:" << std::endl;
  EcUtils::printPoint(cypher);

  // ================== DEC ==================

  // 1. Get x using private key a and point Q. (aQ = a * Q = a * k * P)
  FieldPoint aQ_point = EcOperations::scalarMultiply(a, Q);

  // 2. Get aQ inverse. (aQ = k * a * P)
  FieldPoint dec_aQ_point = FieldPoint(-aQ_point.first, aQ_point.second);

  // 3. Decypher message.
  FieldPoint dec_message = EcOperations::edwardsAdd(dec_aQ_point, cypher);

  std::cout << "Decrypted cypher:" << std::endl;
  EcUtils::printPoint(message);

  EcUtils::assertPointsEqual(message, dec_message);
}

int main(void) {
  setupConsts();
  performEncryptionProcess();
  return 0;
};