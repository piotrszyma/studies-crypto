CC = g++
OPTIONS = -Wall -std=c++14
INCLUDES = -I .
LIBS = -lgmp -lgmpxx
BIN = out
.PHONY: all clean
OBJS = main.o field.o operations.o utils.o

all: ${OBJS}
	${CC} ${OPTIONS} -lgmp -lgmpxx ${OBJS} -o ${BIN}

main.o: main.cpp
	${CC} ${OPTIONS} ${INCLUDES} -c main.cpp

%.o: %.cpp %.h
	${CC} ${OPTIONS} ${INCLUDES} -c $*.cpp

run:
	./${BIN}

clean:
	rm -rf *.o out
