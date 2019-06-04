get_rsa_params:
	openssl rsa -pubin -in cacertificate_pubkey.pem -text -noout

# To get public key from cacertificate.pem
# Requires cacertificate.pem
extract_pubkey:
	openssl x509 -in cacertificate.pem -pubkey -noout > cacertificate_pubkey.pem

# To verify signature (grade.sign) of file (grade.txt) using cacertificate_pubkey.pem
verify_signature:
	openssl dgst -md5 -verify cacertificate_pubkey.pem -signature grade.sign grade.txt

# To verify signature (grade_forged.sign) of file (grade.txt) using cacertificate_pubkey.pem
verify_forged_signature:
	openssl dgst -md5 -verify cacertificate_pubkey.pem -signature grade_generated.sign grade.txt

# Firstly, create cakey.pem using gen_priv_key.py
# Then it requires cakey.pem and grade.txt and will create grade_generated.sign (forged)
create_signature:
	openssl dgst -md5 -sign cakey.pem -out grade_generated.sign grade.txt
