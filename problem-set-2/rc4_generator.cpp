#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include <iostream>
#include <random>
#include <stdint.h>

extern "C" {
    #include "TestU01.h"
}

#define DEFAULT_N 256
#define DEFAULT_T 256
#define DEFAULT_MODE "n"
#define DEFAULT_KEY_LEN 256
#define DEFAULT_DROP_VALUE 8
#define DEFAULT_OUTPUT_LEN 10000


po::variables_map parse_arguments(int argc, char const *argv[]) {
  po::options_description desc("Program that tests RC4 PRNG.");
  desc.add_options()
    ("help", "Help message")
    ("n", po::value<uint16_t>()->default_value(DEFAULT_N), "N value")
    ("mode", po::value<std::string>()->default_value(DEFAULT_MODE), "Mode of operation")
    ("key-len", po::value<uint16_t>()->default_value(DEFAULT_KEY_LEN), "Key length")
    ("drop", po::value<uint16_t>()->default_value(DEFAULT_DROP_VALUE), "Drop value")
    ("test", po::bool_switch()->default_value(false), "Should run tests")
    ("output-len", po::value<uint16_t>()->default_value(DEFAULT_OUTPUT_LEN), "Output size");
  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, desc), vm);
  po::notify(vm);
  if (vm.count("help")) {
    std::cout << desc << std::endl;
  }
  return vm;
}


std::vector<uint16_t> generate_key(uint16_t n) {
  std::random_device rd; // obtain a random number from hardware
  std::mt19937 eng(rd()); // seed the generator

  std::uniform_int_distribution<> distr(0, 255); // define the range
  std::vector<uint16_t> key;
  for (uint16_t i = 0; i < n; i++) {
    key.push_back(distr(eng));
  }
  return key;
}

std::vector<uint16_t> generate_key_perm(std::vector<uint16_t> key, uint16_t n, uint16_t t) {
  std::vector<uint16_t> S;
  for (uint16_t i = 0; i <= n; i++) {
    S.push_back(i);
  }
  // Shuffle S
  uint16_t j = 0;
  uint16_t key_len = key.size();
  for (uint16_t i = 0; i <= t; i++) { // Run loop T+1 times
    j = (j + S[i % n] + key[i % key_len]) % n;
    std::swap(S[i % n], S[j % n]);
  }
  return S;
}

class RC4_PRNG {
  uint16_t i, j, d, n;
  std::vector<uint16_t> s;
  public:
    uint32_t gen() {
      for (uint8_t i = 0; i < d + 1; i++) {
        i = (i + 1) % n;
        j = (j + s[i]) % n;
        std::swap(s[i], s[j]);
      }
      return s[(s[i], s[j]) % n];
    }
    uint32_t gen32bit() {
      uint32_t output = 0;
      for (uint8_t i = 0; i < 4; i++) {
        output += (gen() << (i * 8));
      }
      return output;
    }
    RC4_PRNG(std::vector<uint16_t> s_, uint16_t d_, uint16_t n_) : i(0), j(0), s(s_), d(d_), n(n_) {}
};

// Hacky solution for passing class instance method to extern method.
RC4_PRNG *GLOBAL_PRNG_POINTER;
unsigned int GLOBAL_GEN() {
  return GLOBAL_PRNG_POINTER->gen32bit();
}

char* to_char_ptr(std::string str) {
  char* name = new char[str.size() + 1];
  std::copy(str.begin(), str.end(), name);
  name[str.size()] = '\n';
  return name;
}

int main(int argc, char const *argv[]) {
  po::variables_map parsed_args = parse_arguments(argc, argv);
  if (parsed_args.count("help")) { return 0; }
  uint16_t n = parsed_args["n"].as<uint16_t>();
  std::string mode = parsed_args["mode"].as<std::string>();
  uint16_t t = mode == "n" ? n : 2 * n * std::log(n);
  uint16_t key_len = parsed_args["key-len"].as<uint16_t>();
  uint16_t drop_value = parsed_args["drop"].as<uint16_t>();
  bool run_test = parsed_args["test"].as<bool>();
  uint16_t output_len = parsed_args["output-len"].as<uint16_t>();

  std::vector<uint16_t> key = generate_key(key_len);
  std::vector<uint16_t> s = generate_key_perm(key, n, t);
  RC4_PRNG prng (s, drop_value, n);

  if (run_test) {
    GLOBAL_PRNG_POINTER = &prng;

    unif01_Gen* gen = unif01_CreateExternGenBits(to_char_ptr("RC4 mdrop"), GLOBAL_GEN);
    // Run the tests.
    bbattery_SmallCrush(gen);
    // Clean up.
    unif01_DeleteExternGenBits(gen);
  } else {
    for (uint16_t i = 0; i < output_len; i++) {
        std::cout << prng.gen32bit() << std::endl;
    }
  }
  return 0;
}
