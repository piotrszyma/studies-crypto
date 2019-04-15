MAIN=main.cpp
OUTPUT=main.o
STORE_PASS=testpass
KEY_PASS=testpass
KEY_STORE_NAME=teststore.pkcs12

all: build run

build:
	g++ $(MAIN) -o $(OUTPUT) -l boost_program_options -l crypto

key_gen:
	keytool \
		-genseckey \
		-keypass $(KEY_PASS) \
		-storepass $(STORE_PASS) \
		-alias testkey \
		-keyalg AES \
		-keysize 128 \
		-storetype pkcs12 \
		-keystore $(KEY_STORE_NAME)

key_list:
	@echo "When prompted, insert password: $(KEY_PASS)"
	@keytool \
		-list \
		-keystore $(KEY_STORE_NAME)

key_remove:
	rm $(KEY_STORE_NAME)

run:
	./$(OUTPUT)