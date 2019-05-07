#include <vector>
#include <random>
#include <climits>
#include <iostream>
#include <openssl/aes.h>

#define KEY_SIZE 16 // bytes
#define CONSTANT_SIZE 4

using random_bytes_engine = std::independent_bits_engine<std::default_random_engine, CHAR_BIT, unsigned char>;

random_bytes_engine rbe;

std::vector<unsigned char> generate_random_bytes(int size) {
  std::vector<unsigned char> random_data(size);
  std::generate(begin(random_data), end(random_data), std::ref(rbe));
  return random_data;
}

void generate_single_puzzle(int puzzle_id, std::vector<unsigned char> k1, std::vector<unsigned char> k2, std::vector<unsigned char> constant) {
  std::vector<unsigned char> puzzle_id_bytes;
  for (int i = 0; i < 15; i++) puzzle_id_bytes.push_back(0);
  puzzle_id_bytes.push_back(puzzle_id);
}

void generate_puzzles() {
  std::vector<unsigned char> k1 = generate_random_bytes(KEY_SIZE);
  std::vector<unsigned char> k2 = generate_random_bytes(KEY_SIZE);
  std::vector<unsigned char> constant = generate_random_bytes(CONSTANT_SIZE);
  return;
}

int main(void) {
  return 0;
}
