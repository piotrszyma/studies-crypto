MAIN=rc4_generator.cpp
OUTPUT=rc4_generator.o

all: build run

build:
	g++ $(MAIN) -o $(OUTPUT) -l testu01 -l probdist -l mylib -l gmp -l boost_program_options

run:
	./$(OUTPUT)
