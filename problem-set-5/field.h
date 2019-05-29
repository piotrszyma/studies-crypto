#include <gmpxx.h>

extern mpz_class MPZ_ONE;
extern mpz_class MPZ_ZERO;
extern mpz_class MPZ_TWO;
mpz_class positiveModulo(mpz_class value, mpz_class modulus);

class F {
  private:
    mpz_class value;
    mpz_class modulus;
  public:
    F(mpz_class value_, mpz_class modulus_);

    F(int value_, int modulus_);

    mpz_class getValue();
    mpz_class getModulus();

    F getFromModulus(mpz_class value_);

    F getOne();

    F getD();

    F operator + (F anotherObject);

    F operator - (F anotherObject);

    F operator - ();

    F operator * (F anotherObject);

    F operator / (F anotherObject);

    bool operator == (F anotherObject);

    bool operator != (F anotherObject);
};

typedef std::pair<F, F> F_PAIR;