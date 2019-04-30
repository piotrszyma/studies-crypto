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

perform_challenge:
	python main.py \
	enc \
	--config_path config/config.ini \
	--input_folder=messages \
	--challenge

create_test_data:
	mkdir messages
	echo "message1" > messages/m1
	echo "message2" > messages/m2
	echo "message3" > messages/m3

encrypt_test_data:
	python main.py \
	enc \
	--config_path config/config.ini \
	--input_folder=messages \
	--output_folder=cyphers

decrypt_test_data:
	python main.py \
	dec \
	--config_path config/config.ini \
	--input_folder=cyphers \
	--output_folder=decrypted