#include <iostream>
#include <assert.h>
#include <tuple>

#include "defines.h"
#include "field.h"
#include "operations.h"


FieldNumber::FieldNumber(mpz_class value_, mpz_class modulus_) : value(EcOperations::positiveModulo(value_, modulus_)), modulus(modulus_) {};

FieldNumber::FieldNumber(int value_, int modulus_) : value(mpz_class(EcOperations::positiveModulo(value_, modulus_))), modulus(mpz_class(modulus_)) {};

mpz_class FieldNumber::getValue() {
  return value;
}

mpz_class FieldNumber::getModulus() {
  return modulus;
}

FieldNumber FieldNumber::getFromModulus(mpz_class value_) {
  return FieldNumber(value_, modulus);
}

FieldNumber FieldNumber::getOne() {
  return FieldNumber(mpz_class(1), modulus);
}

FieldNumber FieldNumber::getD() {
  return FieldNumber(mpz_class(EcDefines::EDWARDS_CURVE_D_PARAM), modulus);
}

FieldNumber FieldNumber::operator + (FieldNumber anotherNumber) {
  assert(modulus == anotherNumber.modulus);
  mpz_class thisValue = getValue();
  mpz_class anotherValue = anotherNumber.getValue();
  mpz_class result;
  mpz_add(result.get_mpz_t(), thisValue.get_mpz_t(), anotherValue.get_mpz_t());
  return FieldNumber(result, modulus);
}

FieldNumber FieldNumber::operator - () {
  return FieldNumber(-1, modulus) * FieldNumber(this->getValue(), modulus);
}

FieldNumber FieldNumber::operator - (FieldNumber anotherNumber) {
  assert(modulus == anotherNumber.modulus);
  mpz_class thisValue = getValue();
  mpz_class anotherValue = anotherNumber.getValue();
  mpz_class result;
  mpz_sub(result.get_mpz_t(), thisValue.get_mpz_t(), anotherValue.get_mpz_t());
  return FieldNumber(result, modulus);
}

FieldNumber FieldNumber::operator * (FieldNumber anotherNumber) {
  assert(modulus == anotherNumber.modulus);
  mpz_class thisValue = getValue();
  mpz_class anotherValue = anotherNumber.getValue();
  mpz_class result;
  mpz_mul(result.get_mpz_t(), thisValue.get_mpz_t(), anotherValue.get_mpz_t());
  return FieldNumber(result, modulus);
}

FieldNumber FieldNumber::operator / (FieldNumber anotherNumber) {
  assert(modulus == anotherNumber.modulus);
  mpz_class result;
  mpz_class modulus_less_two;
  mpz_sub(modulus_less_two.get_mpz_t(), modulus.get_mpz_t(), mpz_class(2).get_mpz_t());
  mpz_powm(result.get_mpz_t(), anotherNumber.getValue().get_mpz_t(), modulus_less_two.get_mpz_t(), modulus.get_mpz_t());
  return FieldNumber(this->getValue(), modulus) * FieldNumber(result, modulus);
}

bool FieldNumber::operator == (FieldNumber anotherNumber) {
  return mpz_cmp(getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t()) == 0;
}

bool FieldNumber::operator != (FieldNumber anotherNumber) {
  return mpz_cmp(getValue().get_mpz_t(), anotherNumber.getValue().get_mpz_t()) != 0;
}