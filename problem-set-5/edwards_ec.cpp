#include <iostream>
#include <tuple>
#include <functional>
#include <assert.h>
#include <utility>

#include <gmp.h>

#define ED_CURV_D -300

// Edward curve def
// x_2 + y_2 = 1 + d * x_2 * y_2.

int modInverse(int a, int m) 
{ 
  a = a % m; 
  for (int x=1; x<m; x++) {
    if ((a*x) % m == 1) {
      return x; 
    }
  }
  return -1;
} 

int power(int base, const unsigned int exponent, const int modulus) {
  while (base < 0) 
  if (modulus == 0) { return 0; }
  int result = 1;
  for (unsigned int i = 0; i < exponent; i++) {
    result = (result * base) % modulus;
  }
  return result;
}

int positiveModulo(int value, int modulus) {
  return (value % modulus + modulus) % modulus;
}

class F {
  private:
    int value;
    int modulus;
  public:
    F(int value_, int modulus_) : value(positiveModulo(value_, modulus_)), modulus(modulus_) {};
    int getValue() {
      return value;
    }
    int getModulus() {
      return modulus;
    }

    // Generates new F same modulus with new value.
    F getFromModulus(int value_) {
      return F(value_, modulus);
    }

    F getOne() {
      return F(1, modulus);
    }

    F getD() {
      return F(ED_CURV_D, modulus);
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

auto modulusFactory(int modulus) {
  return [modulus](int number) {
    return F(number, modulus); 
  };
};


auto gen() {
  auto F_1009 = modulusFactory(1009);
  F_PAIR knownPoint (F_1009(1), F_1009(0)); // P
  auto privateKey = 581; // a
  F_PAIR publicKey = scalarMultiply(privateKey, knownPoint); // R
  return std::make_tuple(knownPoint, publicKey, privateKey); // P, R, a
}

auto enc(F message, F_PAIR publicKey, F_PAIR knownPoint) {
  auto randomKey = 223;
  auto decPoint = scalarMultiply(randomKey, knownPoint); // Q = k * P
  auto encPoint = scalarMultiply(randomKey, publicKey); // k * R
  auto cypher = message * encPoint.first;
  return std::make_tuple(cypher, decPoint); // (x * m, Q)
}

auto dec(F cypher, int privateKey, F_PAIR decPoint) {
  F_PAIR privDecPoint = scalarMultiply(privateKey, decPoint);
  F privDecPointX = privDecPoint.first;
  std::cout << privDecPointX.getValue() << std::endl;
  auto modInv = modInverse(privDecPointX.getValue(), 1009);
  std::cout << modInv << std::endl;
};


int main(void) {
  // Generate random modulus;
  mpz_t randomNumber;
  unsigned long int i, seed;
  gmp_randstate_t r_state;
  seed = 123456;
  gmp_randinit_default(r_state);
  gmp_randseed_ui(r_state, seed);
  mpz_init(randomNumber);

  for(i = 0; i < 10; ++i) {
      mpz_urandomb(randomNumber,r_state,256);
  }

  gmp_randclear(r_state);
  mpz_clear(randomNumber);


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


  // auto F_1009 = modulusFactory(1009);
  // assert(F_1009(-1) == F_1009(1008));
  // assert(F_1009(6) != F_1009(5));
  // assert(F_1009(101) + F_1009(1000) == F_1009(92));
  // assert(F_1009(101) - F_1009(1000) == F_1009(110));
  // assert(F_1009(101) * F_1009(1000) == F_1009(100));
  // assert(F_1009(101) / F_1009(1000) == F_1009(213));
  
  // F_PAIR P1 (F_1009(7), F_1009(415));
  // F_PAIR P2 (F_1009(23), F_1009(487));
  // F_PAIR result = edwardsAdd(P1, P2);

  // assert(result.first.getValue() == 944);
  // assert(result.second.getValue() == 175);

  // F_PAIR multResult = scalarMultiply(5, result);
  // assert(multResult.first.getValue() == 900);
  // assert(multResult.second.getValue() == 799);
  return 0;
};