import base64
import configparser
import jks
import OpenSSL


SECRET_PASSWORD = 'testpass'
CONFIG_PATH = 'config/config.ini'
KEYSTORE_PATH = 'data/keystore.jks'
PRIVKEY_NAME = 'encryption key'

def generate_key(length=2048):
  key = OpenSSL.crypto.PKey()
  key.generate_key(OpenSSL.crypto.TYPE_RSA, length)
  return OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, key)

def save_to_keystore(dumped_key, keystore_path, secret_password):
  pke = jks.PrivateKeyEntry.new(PRIVKEY_NAME, [], dumped_key, 'rsa_raw')
  keystore = jks.KeyStore.new('jks', [pke])
  keystore.save(keystore_path, secret_password)

def load_key_from_keystore(keystore_path, secret_password):
  keystore = jks.KeyStore.load(keystore_path, secret_password)
  key_bytes =  keystore.private_keys[PRIVKEY_NAME].pkey
  return key_bytes


if __name__ == "__main__":
  config = configparser.ConfigParser()
  config.read(CONFIG_PATH)
  credentials_config = config['credentials']
  keystore_path = credentials_config.get('keystore')
  secret_password = credentials_config['password']
  dumped_key = generate_key()
  save_to_keystore(
      dumped_key,
      keystore_path=keystore_path,
      secret_password=secret_password)
