test:
	python3 -m unittest libs.crypto_libs_test


STORE_PASS=testpass
KEY_STORE_NAME=data/keystore.jks

key_gen:
	keytool \
		-genseckey \
		-keypass $(KEY_PASS) \
		-storepass $(STORE_PASS) \
		-alias encryption\ key \
		-keyalg AES \
		-keysize 128 \
		-storetype jks \
		-keystore $(KEY_STORE_NAME)