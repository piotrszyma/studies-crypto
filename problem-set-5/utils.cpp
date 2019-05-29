#include "utils.h"

#include <iostream>

namespace EcUtils {
  void printPoint(FieldPoint point) {
    std::cout << "(" << point.first.getValue().get_mpz_t() << ", ";
    std::cout << point.second.getValue().get_mpz_t() << ")" << std::endl;
  }
}
