/* RC4 testu01
Build with: g++ -std=c++17 rc4_testu01.cpp -o test01.o -ltestu01 -lprobdist -lmylib -lgmp
Based on: http://www.pcg-random.org/posts/how-to-test-with-testu01.html
*/

#include <iostream>
#include <array>
#include <vector>

extern "C" {
    #include "TestU01.h"
}

// BEGIN DEFINITIONS
#define D_VALUE 0
#define N_VALUE 256
#define T_VALUE 256
static const unsigned int key[] = { 33, 99, 121, 67, 59, 228, 68, 242, 128, 174, 40, 126, 2, 22, 26, 123, 222, 209, 176, 4, 44, 95, 30, 222, 95, 5, 45, 208, 158, 189, 102, 114, 242, 36, 165, 10, 141, 101, 68, 61 };
// END DEFINITIONS

static unsigned int KEY_LEN = sizeof(key) / sizeof(int);

static std::vector<int> S;
static unsigned int PRGA_I = 0;
static unsigned int PRGA_J = 0;

void KSA(const int N, const int T) {
  // Initialize S with 0...n
  S.clear();
  for (unsigned int i = 0; i <= N; i++) {
    S.push_back(i);
  }

  // Shuffle S
  unsigned int j = 0;
  for (unsigned int i = 0; i <= T; i++) { // Run loop T+1 times
    j = (j + S[i % N] + key[i % KEY_LEN]) % N;
    std::swap(S[i % N], S[j % N]);
  }
}

unsigned int PRGA() {
  // Run loops D_VALUE + 1 times.
  for (int i = 0; i < D_VALUE+1; i++) {
    PRGA_I = (PRGA_I + 1) % N_VALUE;
    PRGA_J = (PRGA_J + S[PRGA_I]) % N_VALUE;
    std::swap(S[PRGA_J], S[PRGA_I]);
  }
  return S[(S[PRGA_J] + S[PRGA_I]) % N_VALUE];
}


int main()
{
  KSA(N_VALUE, N_VALUE);

  // for (int i = 0; i < 10; i++) {
  //   std::cout << PRGA() << "\n";
  // }

  // Create TestU01 PRNG object for our generator
  unif01_Gen* gen = unif01_CreateExternGenBits("RC4 mdrop", PRGA);

  // Run the tests.
  bbattery_SmallCrush(gen);

  // Clean up.
  unif01_DeleteExternGenBits(gen);
  return 0;
}