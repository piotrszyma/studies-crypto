#include <iostream>
#include <stdexcept>
#include <functional>
#include <fstream>
#include <boost/program_options.hpp>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <openssl/pkcs12.h>

namespace po = boost::program_options;
const static unsigned char aes_key[]={0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xAA,0xBB,0xCC,0xDD,0xEE,0xFF};


std::vector<char> read_file_bytes(std::string filepath) {
  std::ifstream ifstream_object(filepath, std::ifstream::binary | std::ifstream::ate);
  std::ifstream::pos_type position = ifstream_object.tellg();
  std::vector<char> result(position);
  ifstream_object.seekg(0, std::ifstream::beg);
  ifstream_object.read(&result[0], position);
  return result;
}

void read_secret_key(std::string filepath) {
  FILE *fp;
  PKCS12 *p12;
  EVP_PKEY *pkey = NULL;
  // X509 *cert = NULL;
  // STACK_OF(X509) *ca = NULL;
  OpenSSL_add_all_algorithms(); // TODO: Move it to some crypto_init method?
  if ((fp = fopen("teststore.pkcs12", "rb")) == NULL) {
      std::cout << "Failed to open teststore." << std::endl;
  } else {
      std::cout << "Test store opened." << std::endl;
  }
  p12 = d2i_PKCS12_fp(fp, NULL);
  PKCS12_free(p12);
  PKCS12_parse(p12, "testpass", &pkey, NULL, NULL);
  fclose(fp);
}


void encrypt_AES_cbc_encrypt() {
  /* Input data to encrypt */
	unsigned char aes_input[]={0x0,0x1,0x2,0x3,0x4,0x5};
	
	/* Init vector */
	unsigned char iv[AES_BLOCK_SIZE];
	memset(iv, 0x00, AES_BLOCK_SIZE);
	
	/* Buffers for Encryption and Decryption */
	unsigned char enc_out[sizeof(aes_input)];
	unsigned char dec_out[sizeof(aes_input)];
	
	/* AES-128 bit CBC Encryption */
	AES_KEY enc_key, dec_key;
	AES_set_encrypt_key(aes_key, sizeof(aes_key)*8, &enc_key);
	AES_cbc_encrypt(aes_input, enc_out, sizeof(aes_input), &enc_key, iv, AES_ENCRYPT);
	/* AES-128 bit CBC Decryption */
	memset(iv, 0x00, AES_BLOCK_SIZE); // don't forget to set iv vector again, else you can't decrypt data properly
	AES_set_decrypt_key(aes_key, sizeof(aes_key)*8, &dec_key); // Size of key is in bits
	AES_cbc_encrypt(enc_out, dec_out, sizeof(aes_input), &dec_key, iv, AES_DECRYPT);
	
	/* Printing and Verifying */
	// print_data("\n Original ",aes_input, sizeof(aes_input)); // you can not print data as a string, because after Encryption its not ASCII
	
	// print_data("\n Encrypted",enc_out, sizeof(enc_out));
	
	// print_data("\n Decrypted",dec_out, sizeof(dec_out));
	
  return;
}


po::variables_map parse_arguments(int argc, char const *argv[]) {
  po::options_description desc("Program that tests RC4 PRNG.");
  desc.add_options()
    ("help", "Help message")
    ("input", po::value<std::string>(), "Input path")
    ("keystroke", po::value<std::string>(), "Keystroke path")
    ("mode", po::value<std::string>(), "Encryption mode")
    // ("n", po::value<uint16_t>()->default_value(DEFAULT_N), "N value")
    // ("mode", po::value<std::string>()->default_value(DEFAULT_MODE), "Mode of operation")
    // ("key-len", po::value<uint16_t>()->default_value(DEFAULT_KEY_LEN), "Key length")
    // ("drop", po::value<uint16_t>()->default_value(DEFAULT_DROP_VALUE), "Drop value")
    // ("test", po::bool_switch()->default_value(false), "Should run tests")
    ("output", po::value<std::string>(), "Output path");
  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, desc), vm);
  po::notify(vm);
  if (vm.count("help")) {
    std::cout << desc << std::endl;
  }
  return vm;
}


std::function<void(void)> encrypt_mode(const std::string mode) {
  if (mode == "openssl_aes_cbc") {
    return encrypt_AES_cbc_encrypt;
  } else {
    throw std::invalid_argument("Unknown encrypton mode.");
  }
}


int main(const int argc, const char *argv[])
{
  read_secret_key("test");
  // po::variables_map vm = parse_arguments(argc, argv);
  // if (vm.count("help")) return 0;
  // const std::string mode = vm["mode"].as<std::string>();
  // std::function<void(void)> encryption_function = encrypt_mode(mode);
  return 0;
}
