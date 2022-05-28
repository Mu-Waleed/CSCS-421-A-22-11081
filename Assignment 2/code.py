#importing the necessary modules

import ast
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import pickle


# method to print the content of file
def print_file(fileName):
    print("")
    f = open(fileName, "r")
    print("Text in file:")
    print(f.read())
    print("")

# method to perform encryption or decryption
def process(user, fileName):
    if user == 1:
        public_key, key = generateKey()
        time_opened = 0
        text = ""
        print('encrypted message: ')
        with open(fileName, "r") as file:
            for line in file.readlines():
                text += line
            time_opened = encrypt(fileName, text, time_opened, public_key)

    if user == 2:
        public_key, key = read_keys()
        time_opened = 0
        print('Decrypted message:\n')
        f = open(fileName, 'r')
        message = ""
        for line in f.readlines():
            message += line
        time_opened = decrypt(fileName, message, time_opened, key)
            

# Generate public and private key
def generateKey():
    key = RSA.generate(1024)
    public_key = key.publickey()
    with open("public_key.pem", "wb") as outp:
        outp.write(public_key.export_key("PEM"))

    with open("key.pem", "wb") as outp:
        outp.write(key.export_key("PEM"))
 
    return public_key, key

# read the keys
def read_keys():
    with open('public_key.pem', 'r') as inp:
        public_key = RSA.import_key(inp.read())

    with open('key.pem', 'r') as inp:
        key = RSA.import_key(inp.read())
        
    return public_key, key

# perform encryption
def encrypt(fileName, message, time_opened, public_key):
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted = encryptor.encrypt(message.encode())
    print(encrypted)

    if time_opened == 0:
        time_opened += 1
        f = open ('encryption.txt', 'w')
        f.write(str(encrypted) + "\n")
        f.close()

    else:
        f = open ('encryption.txt', 'a')
        f.write(str(encrypted) + "\n")
        f.close()

    print("Saved Encryption in encryption.txt!")
    return time_opened

# perform decryption
def decrypt(fileName, message, time_opened, key):
    decryptor = PKCS1_OAEP.new(key)
    decrypted = decryptor.decrypt(ast.literal_eval(str(message)))
    time_opened = 0
    print(decrypted.decode())
    
    return time_opened


# method to combine all methods
def main(text):
    user = input(text)
    try:
        if ".txt" in user and enc == True:
            print_file(user)
            process(1, user)
            
        elif enc == True:
            public_key, key = generateKey()
            print("")
            print("encrypted message:")
            timed = encrypt("encryption.txt", user,0, public_key)
            
        elif enc == False:
            print("")
            process(2, user)

        print("")

    except:
        print("Wrong File name: \n")
        
text = ""
while True:
    print("1) Apply Encryption ")
    print("2) Apply Decryption ")
    print("3) Exit \n")

    user = input("Type 1,2 or 3: ")
    print("")
    enc = False
    if user == str(3):
        break
    
    elif user == str(1):
        text = "Type the message or name of the text file with .txt: "
        enc = True
        main(text)

    elif user == str(2):
        text = "Type name of the encrypted file with .txt: "
        main(text)

    else:
        print("Wrong Input!")
    


