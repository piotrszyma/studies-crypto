all: build run

build:
	gcc glibc_random.c -o glibc_random

debug:
	gcc -g -o glibc_random_debug glibc_random.c

run_debug:
	gdb glibc_random_debug

run:
	./glibc_random
