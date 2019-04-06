/* RC4 testu01
Build with: g++ -std=c++17 rc4_testu01.cpp -o test01.o -ltestu01 -lprobdist -lmylib -lgmp
Based on: http://www.pcg-random.org/posts/how-to-test-with-testu01.html
*/

#include <iostream>
#include <array>
#include <vector>
#include <iomanip>
#include <sstream>
#include <fstream>
#include <random>

extern "C" {
    #include "TestU01.h"
}

// BEGIN DEFINITIONS
#define D_VALUE 16
#define N_VALUE 256
#define T_VALUE 256
// #define OUT_SIZE 1000
// #define OUT_FILE "test_file.txt"
// static const unsigned int key[] = { 33, 99, 121, 67, 59, 228, 68, 242, 128, 174, 40, 126, 2, 22, 26, 123, 222, 209, 176, 4, 44, 95, 30, 222, 95, 5, 45, 208, 158, 189, 102, 114, 242, 36, 165, 10, 141, 101, 68, 61 };
// static const unsigned int key[] = { 67, 8, 135, 176, 198, 198, 204, 86, 86, 41, 74, 27, 201, 195, 77, 125, 180, 132, 182, 79, 219, 125, 32, 74, 122, 171, 165, 222, 79, 98, 33, 194, 82, 54, 160, 209, 224, 84, 250, 214, 92, 108, 166, 46, 172, 151, 125, 60, 147, 150, 15, 105, 2, 72, 201, 209, 100, 219, 58, 195, 75, 245, 169, 205, 54, 162, 87, 193, 198, 85, 180, 42, 82, 62, 255, 219, 104, 143, 240, 245, 39, 240, 128, 248, 128, 201, 241, 165, 25, 109, 99, 175, 156, 137, 1, 19, 56, 88, 49, 91, 49, 40, 231, 46, 249, 215, 70, 185, 192, 133, 141, 75, 39, 70, 158, 109, 148, 192, 149, 71, 64, 195, 2, 227, 20, 125, 18, 61 };
// static const unsigned int key[] = { 53, 73, 233, 50, 212, 108, 131, 190, 176, 2, 244, 214, 206, 168, 14, 151, 102, 156, 100, 67, 44, 172, 172, 130, 220, 27, 121, 32, 85, 159, 208, 8, 146, 156, 200, 25, 185, 70, 149, 90, 152, 13, 51, 173, 58, 41, 160, 47, 194, 121, 33, 143, 105, 199, 74, 2, 212, 147, 149, 151, 161, 239, 79, 233, 162, 247, 138, 228, 7, 234, 40, 34, 61, 67, 129, 203, 249, 84, 67, 53, 201, 187, 32, 124, 159, 90, 58, 8, 2, 186, 15, 160, 17, 26, 98, 99, 18, 86, 49, 168, 228, 169, 155, 209, 185, 119, 208, 58, 35, 132, 84, 87, 9, 191, 151, 92, 143, 4, 5, 235, 146, 32, 114, 133, 44, 170, 158, 93, 249, 167, 20, 168, 59, 117, 250, 144, 65, 238, 7, 110, 127, 148, 14, 36, 30, 71, 75, 4, 251, 35, 27, 38, 50, 11, 24, 112, 37, 102, 146, 94, 21, 250, 83, 107, 119, 164, 163, 203, 73, 201, 50, 117, 105, 34, 2, 15, 169, 248, 80, 106, 162, 56, 220, 232, 177, 95, 69, 80, 81, 182, 119, 205, 43, 172, 64, 119, 109, 209, 143, 195, 36, 149, 116, 169, 145, 96, 14, 60, 165, 193, 51, 105, 167, 211, 172, 187, 213, 46, 62, 40, 41, 11, 227, 91, 60, 214, 145, 243, 212, 123, 8, 125, 227, 50, 70, 25, 210, 87, 216, 99, 206, 97, 42, 98, 199, 229, 192, 104, 194, 111, 48, 151, 96, 179, 139, 137 };
// END DEFINITIONS

unsigned int get_random_byte() {
    std::random_device dev;
    std::mt19937 rng(dev());
    std::uniform_int_distribution<std::mt19937::result_type> dist6(0, 255); // distribution in range [1, 6]
    return dist6(rng);
}

std::vector<int> get_random_bytes(const int size) {
  std::vector<int> key;
  for (int i = 0; i < size; i ++) {
    key.push_back(get_random_byte());
  }
  return key;
}

std::vector<int> KSA(std::vector<int> key, const int N, const int T) {
  // Initialize S with 0...n
  const int KEY_LEN = key.size();
  std::vector<int> S;
  for (unsigned int i = 0; i <= N; i++) { S.push_back(i); }

  // Shuffle S
  unsigned int j = 0;
  for (unsigned int i = 0; i <= T; i++) { // Run loop T+1 times
    j = (j + S[i % N] + key[i % KEY_LEN]) % N;
    std::swap(S[i % N], S[j % N]);
  }
  return S;
}

static std::vector<int> PRGA_S;
static unsigned int PRGA_I = 0;
static unsigned int PRGA_J = 0;

unsigned int PRGA() {
  // Run loops D_VALUE + 1 times.
  for (int i = 0; i < D_VALUE + 1; i++) {
    PRGA_I = (PRGA_I + 1) % N_VALUE;
    PRGA_J = (PRGA_J + PRGA_S[PRGA_I]) % N_VALUE;
    std::swap(PRGA_S[PRGA_J], PRGA_S[PRGA_I]);
  }
  return PRGA_S[(PRGA_S[PRGA_J] + PRGA_S[PRGA_I]) % N_VALUE];
}

unsigned int PRGA_32BIT() {
  unsigned int left = PRGA();
  unsigned int middle = PRGA() << 8;
  unsigned int right = PRGA() << 16;
  return left + middle + right;
}


int main()
{
  std::vector<int> key = get_random_bytes(256);
  std::vector<int> S = KSA(key, N_VALUE, T_VALUE);

  PRGA_S = S;

  // KSA(N_VALUE, T_VALUE);

  // std::ostringstream sstr;

  // std::ofstream myfile;
  // myfile.open(OUT_FILE, std::ios::binary);
  // myfile << "#==================================================================\n# test_#{mode}_#{n}_#{t}_#{d}_#{length(k)}\n#==================================================================\ntype: d\ncount: " <<OUT_SIZE<< "\nnumbit: "<< OUT_BIT <<"\n";

  // long long i = 0;

  // for (unsigned long long iii = 1; i < OUT_SIZE; iii++) {
  //   myfile << (char) PRGA();
  //   if (!(iii % 10000)) {
  //     myfile.flush();
  //     i++;
  //   }
  // }
  // myfile.close();
  // std::cout <<
  // "#==================================================================\n"
  // "# generator mt19937  seed = 281536748\n"
  // "#==================================================================\n"
  // "type: d\n"
  // "count: 10000000\n"
  // "numbit: 32\n";
  // for (int i = 0; i < 10000000; i++) {
  //   std::cout << std::setfill(' ') << std::setw(8) << PRGA_32BIT() << "\n";
  // }

  // show_details();

  // Create TestU01 PRNG object for our generator
  unif01_Gen* gen = unif01_CreateExternGenBits("RC4 mdrop", PRGA_32BIT);
  // Run the tests.
  bbattery_SmallCrush(gen);
  // Clean up.
  unif01_DeleteExternGenBits(gen);


  // show_details();
  return 0;
}