#include <iostream>
#include <assert.h>
#include <tuple>

#include "field.h"

#define ED_CURV_D -11

mpz_class MPZ_ZERO(0);
mpz_class MPZ_ONE(1);
mpz_class MPZ_TWO(2);


// mpz_class power(mpz_class base, mpz_class exponent, mpz_class modulus) {
//   if (mpz_cmp(modulus.get_mpz_t(), MPZ_ZERO.get_mpz_t()) < 0) {
//     assert(1 == 0);
//   }
//   if (mpz_cmp(modulus.get_mpz_t(), MPZ_ZERO.get_mpz_t()) == 0) { return mpz_class(0); }
//   mpz_class result;
//   mpz_class cache;
//   for (mpz_class i(0); mpz_cmp(i.get_mpz_t(), exponent.get_mpz_t()) < 0; mpz_add(i.get_mpz_t(), i.get_mpz_t(), MPZ_ONE.get_mpz_t())) {
//     // result = result * base;
//     mpz_mul(cache.get_mpz_t(), result.get_mpz_t(), base.get_mpz_t());
//     // result = result % modulus;
//     mpz_mod(result.get_mpz_t(), cache.get_mpz_t(), modulus.get_mpz_t());
//   }
//   return mpz_class(result);
// }

mpz_class positiveModulo(mpz_class value, mpz_class modulus) {
  mpz_class result1, result2, result3;
  mpz_mod(result1.get_mpz_t(), value.get_mpz_t(), modulus.get_mpz_t());
  return result1;
  // return (value % modulus + modulus) % modulus;
}

F::F(mpz_class value_, mpz_class modulus_) : value(positiveModulo(value_, modulus_)), modulus(modulus_) {};

F::F(int value_, int modulus_) : value(mpz_class(positiveModulo(value_, modulus_))), modulus(mpz_class(modulus_)) {};

mpz_class F::getValue() {
  return value;
}

mpz_class F::getModulus() {
  return modulus;
}

F F::getFromModulus(mpz_class value_) {
  return F(value_, modulus);
}

F F::getOne() {
  return F(MPZ_ONE, modulus);
}

F F::getD() {
  return F(mpz_class(ED_CURV_D), modulus);
}

F F::operator + (F anotherObject) {
  assert(modulus == anotherObject.modulus);
  mpz_class thisValue = getValue();
  mpz_class anotherValue = anotherObject.getValue();
  mpz_class result;
  mpz_add(result.get_mpz_t(), thisValue.get_mpz_t(), anotherValue.get_mpz_t());
  return F(result, modulus);
}

F F::operator - () {
  return F(-1, modulus) * F(this->getValue(), modulus);
}

F F::operator - (F anotherObject) {
  assert(modulus == anotherObject.modulus);
  mpz_class thisValue = getValue();
  mpz_class anotherValue = anotherObject.getValue();
  mpz_class result;
  mpz_sub(result.get_mpz_t(), thisValue.get_mpz_t(), anotherValue.get_mpz_t());
  return F(result, modulus);
}

F F::operator * (F anotherObject) {
  assert(modulus == anotherObject.modulus);
  mpz_class thisValue = getValue();
  mpz_class anotherValue = anotherObject.getValue();
  mpz_class result;
  mpz_mul(result.get_mpz_t(), thisValue.get_mpz_t(), anotherValue.get_mpz_t());
  return F(result, modulus);
}

F F::operator / (F anotherObject) {
  assert(modulus == anotherObject.modulus);
  mpz_class result;
  mpz_class modulus_less_two;
  mpz_sub(modulus_less_two.get_mpz_t(), modulus.get_mpz_t(), MPZ_TWO.get_mpz_t());
  mpz_powm(result.get_mpz_t(), anotherObject.getValue().get_mpz_t(), modulus_less_two.get_mpz_t(), modulus.get_mpz_t());
  return F(this->getValue(), modulus) * F(result, modulus);
}

bool F::operator == (F anotherObject) {
  // std::cout << getValue().get_mpz_t() << std::endl;
  // std::cout << anotherObject.getValue().get_mpz_t() << std::endl;
  return mpz_cmp(getValue().get_mpz_t(), anotherObject.getValue().get_mpz_t()) == 0;
}

bool F::operator != (F anotherObject) {
  return mpz_cmp(getValue().get_mpz_t(), anotherObject.getValue().get_mpz_t()) != 0;
}