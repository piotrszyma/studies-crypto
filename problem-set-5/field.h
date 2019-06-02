#ifndef FIELD_H
#define FIELD_H

#include <gmpxx.h>

class FieldNumber {
  private:
    mpz_class value;
    mpz_class modulus;
  public:
    static mpz_class D_VALUE;
    static mpz_class I_VALUE;
    static mpz_class MODULUS;

    FieldNumber();
    FieldNumber(mpz_class value_);
    FieldNumber(mpz_class value_, mpz_class modulus_);
    FieldNumber(int value_, int modulus_);

    mpz_class getValue();
    mpz_class getModulus();

    FieldNumber getFromModulus(mpz_class value_);

    FieldNumber getOne();

    FieldNumber getZero();

    FieldNumber getN(int value);

    FieldNumber getD();

    FieldNumber operator + (FieldNumber anotherNumber);

    FieldNumber operator - (FieldNumber anotherNumber);

    FieldNumber operator - ();

    FieldNumber operator * (FieldNumber anotherNumber);

    FieldNumber operator / (FieldNumber anotherNumber);

    FieldNumber operator % (FieldNumber anotherNumber);

    bool operator == (FieldNumber anotherNumber);

    bool operator != (FieldNumber anotherNumber);
};

typedef std::pair<FieldNumber, FieldNumber> FieldPoint;

#endif //FIELD_H