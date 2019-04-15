MAIN=main.cpp
OUTPUT=main.o

all: build run

build:
	g++ $(MAIN) -o $(OUTPUT) -l boost_program_options -l crypto

run:
	./$(OUTPUT)