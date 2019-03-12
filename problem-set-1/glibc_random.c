#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


int main(int argc, char *argv[]) {
  if (argc < 2 || argc > 3) {
    return 0;
  }
  if (argc == 3) {
    srand(atoi(argv[2]));
  }
  for (int i = 0; i < atoi(argv[1]); i++) {
    printf("%d\n", rand());
  }
  return 0;
}