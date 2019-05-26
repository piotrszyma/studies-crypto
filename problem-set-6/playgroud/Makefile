all: gen_priv_key gen_req

gen_priv_key:
	openssl genrsa -out priv_key.pem 360

gen_req:
	openssl req -new -md5 -key priv_key.pem -subj '/CN=www.mydom.com/O=My Company Name LTD./C=US'