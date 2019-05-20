#include <iostream>
#include <tuple>
#include <functional>
#include <assert.h>
#include <utility>

#define kPameterD -11

// x2+y2=1+dx2y2.

int power(int base, const unsigned int exponent, const int modulus) {
  while (base < 0) 
  if (modulus == 0) { return 0; }
  int result = 1;
  for (unsigned int i = 0; i < exponent; i++) {
    result = (result * base) % modulus;
  }
  return result;
}

int positive_modulo(int value, int modulus) {
  return (value % modulus + modulus) % modulus;
}


class F {
  private:
    int value;
    int modulus;
  public:
    F(int value_, int modulus_) : value(positive_modulo(value_, modulus_)), modulus(modulus_) {};
    int getValue() {
      return value;
    }
    int getModulus() {
      return modulus;
    }

    F getOne() {
      return F(1, modulus);
    }

    F getD() {
      return F(kPameterD, modulus);
    }

    F operator + (F anotherObject) {
      assert(modulus == anotherObject.modulus);
      return F(getValue() + anotherObject.getValue(), modulus);
    }

    F operator - (F anotherObject) {
      assert(modulus == anotherObject.modulus);
      return F(getValue() - anotherObject.getValue(), modulus);
    }

    F operator * (F anotherObject) {
      assert(modulus == anotherObject.modulus);
      return F(getValue() * anotherObject.getValue(), modulus);
    }

    F operator / (F anotherObject) {
      assert(modulus == anotherObject.modulus);
      // Assumes that group is of prime number.
      // X^{-1} % M = (X ^ (M - 2)) % M.
      return F(this->getValue(), modulus) * F(power(anotherObject.getValue(), modulus - 2, modulus), modulus); 
    }

    bool operator == (F anotherObject) {
      return getValue() == anotherObject.getValue(); 
    }

    bool operator != (F anotherObject) {
      return getValue() != anotherObject.getValue();
    }
};

typedef std::pair<F, F> F_PAIR;

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

auto modulus_factory(int modulus) {
  return [modulus](int number) {
    return F(number, modulus); 
  };
};


int main(void) {
  auto F_1009 = modulus_factory(1009);
  assert(F_1009(-1) == F_1009(1008));
  assert(F_1009(6) != F_1009(5));
  assert(F_1009(101) + F_1009(1000) == F_1009(92));
  assert(F_1009(101) - F_1009(1000) == F_1009(110));
  assert(F_1009(101) * F_1009(1000) == F_1009(100));
  assert(F_1009(101) / F_1009(1000) == F_1009(213));
  
  
  F_PAIR P1 (F_1009(7), F_1009(415));
  F_PAIR P2 (F_1009(23), F_1009(487));
  F_PAIR result = edwardsAdd(P1, P2);

  assert(result.first.getValue() == 944);
  assert(result.second.getValue() == 175);

  return 0;
};