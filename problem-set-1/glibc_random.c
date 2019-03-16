#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  if (argc < 2) {
    return 0;
  }

  int amount = atoi(argv[1]);
  int upper_limit = 344 + amount;
  int r[upper_limit];
  int i;

  if (argc == 3) {
    r[0] = atoi(argv[2]);
  } else {
    // Seed
    r[0] = 1;
  }

  for (i=1; i<31; i++) {
    r[i] = (16807LL * r[i-1]) % 2147483647;
    if (r[i] < 0) {
      r[i] += 2147483647;
    }
  }
  for (i=31; i<34; i++) {
    r[i] = r[i-31];
  }
  for (i=34; i<344; i++) {
    r[i] = r[i-31] + r[i-3];
  }
  for (i=344; i < upper_limit; i++) {
    r[i] = r[i-31] + r[i-3];
    printf("%d\n", ((unsigned int)r[i]) >> 1);
  }
  return 0;
}