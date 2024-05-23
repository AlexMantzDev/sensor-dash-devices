import json
import ucryptolib
import ubinascii
import random

class NetworkCredentials:
    default_ssid = "network"
    default_password = "password"
    ssid = default_ssid
    password = default_password
    credentials_file = 'network-credentials.json'
    key_file = 'secret.key'
    key = None
    
    @classmethod
    def generate_key(cls):
        print("Generating key...")
        key = b''.join(random.getrandbits(32).to_bytes(4, 'big') for _ in range(4))
        key_hex = ubinascii.hexlify(key).decode()
        with open(cls.key_file, 'w') as key_file:
            key_file.write(key_hex)
        print(f"Generated key: {key_hex}")
        return key

    @classmethod
    def load_key(cls):
        try:
            print("Loading key...")
            with open(cls.key_file, 'r') as key_file:
                key_hex = key_file.read()
                cls.key = ubinascii.unhexlify(key_hex.encode())
                if len(cls.key) != 16:
                    print("Loaded key has invalid length, regenerating key.")
                    cls.key = cls.generate_key()
                else:
                    print(f"Loaded key: {key_hex}")
        except OSError:
            print("Key file not found, generating a new key.")
            cls.key = cls.generate_key()
        except ValueError as e:
            print(f"Error loading key: {e}, regenerating key.")
            cls.key = cls.generate_key()

    @classmethod
    def encrypt(cls, plaintext):
        if cls.key is None:
            cls.load_key()
        if len(cls.key) != 16:
            raise ValueError("Invalid key length for encryption")
        aes = ucryptolib.aes(cls.key, 1)  # 1 means ECB mode
        pad_length = 16 - (len(plaintext) % 16)
        padded_plaintext = plaintext + chr(pad_length) * pad_length
        encrypted = aes.encrypt(padded_plaintext)
        encrypted_hex = ubinascii.hexlify(encrypted).decode()
        print(f"Encrypted plaintext: {encrypted_hex}")
        return encrypted_hex

    @classmethod
    def decrypt(cls, ciphertext):
        if cls.key is None:
            cls.load_key()
        if len(cls.key) != 16:
            raise ValueError("Invalid key length for decryption")
        aes = ucryptolib.aes(cls.key, 1)  # 1 means ECB mode
        encrypted_bytes = ubinascii.unhexlify(ciphertext.encode())
        decrypted = aes.decrypt(encrypted_bytes)
        pad_length = decrypted[-1]
        decrypted_text = decrypted[:-pad_length].decode()
        print(f"Decrypted ciphertext: {decrypted_text}")
        return decrypted_text

    @classmethod
    def set_credentials(cls, ssid, password):
        print(f"Setting credentials: SSID={ssid}, Password={password}")
        cls.ssid = ssid
        cls.password = cls.encrypt(password)
        cls.save_credentials()

    @classmethod
    def get_credentials(cls):
        decrypted_password = cls.decrypt(cls.password)
        print(f"Getting credentials: SSID={cls.ssid}, Password={decrypted_password}")
        return cls.ssid, decrypted_password

    @classmethod
    def save_credentials(cls):
        credentials = {'ssid': cls.ssid, 'password': cls.password}
        with open(cls.credentials_file, 'w') as file:
            json.dump(credentials, file)
        print(f"Credentials saved: {credentials}")

    @classmethod
    def load_credentials(cls):
        try:
            print("Loading credentials...")
            with open(cls.credentials_file, 'r') as file:
                credentials = json.load(file)
                cls.ssid = credentials.get('ssid', cls.default_ssid)
                cls.password = credentials.get('password', cls.default_password)
                print(f"Loaded credentials: {credentials}")
        except OSError:
            print("Credentials file not found, using default credentials.")
            cls.ssid = cls.default_ssid
            cls.password = cls.default_password
        except json.JSONDecodeError:
            print("Invalid credentials file, using default credentials.")
            cls.ssid = cls.default_ssid
            cls.password = cls.default_password
        
    @classmethod
    def credentials_exist(cls):
        try:
            with open(cls.credentials_file, 'r') as file:
                credentials = json.load(file)
                return True
        except OSError:
            return False

NetworkCredentials.load_credentials()

