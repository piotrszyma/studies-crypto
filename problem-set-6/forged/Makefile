generate_forged_sign:
	openssl dgst -md5 -sign cakey.pem -out grade_forged.sign grade.txt

verify_signature:
	openssl dgst -md5 -verify cacertificate_pubkey.pem -signature grade_forged.sign grade_forged.txt
