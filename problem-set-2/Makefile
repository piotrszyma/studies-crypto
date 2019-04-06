all: build run

build:
	g++ -std=c++17 rc4_testu01.cpp -o test01.o -ltestu01 -lprobdist -lmylib -lgmp

run:
	./test01.o

MAIN=rc4_generator.cpp
OUTPUT=rc4_generator.o

gen_all: build run

gen_build:
	g++ $(MAIN) -o $(OUTPUT) -l boost_program_options

gen_run:
	./$(OUTPUT)
