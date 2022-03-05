import os, re, struct, base64, hashlib
from cryptography.fernet import Fernet
from cryptography import *
import cryptography
from binascii import Error

def Menu(_key):
    os.system("cls")
    print("Options:\n\nLoad key [lk]\nWrite key [wk]\nCreate a random key [rk]\nUse a custom key [ck]\nBefore you can encrypt [ef] a file you have to setup a key\nBefore you can decrypt [df] a file you have to setup a key\n")
    command = input("Enter command: ")
    if command == "wk":
        os.system("cls")
        _key = WriteKey()
        print("Your new key: ",_key,"\nKey written to: ",os.getcwd()+"/key")
        input("Press enter to continue with this key")
        Menu("")
    if command == "lk":
        os.system("cls")
        _key = LoadKey()
        print("Key loaded: ", _key)
        input("Press enter to continue with this key")
        Menu(_key)
    if command == "rk":
        os.system("cls")
        key = Fernet.generate_key()
        _key = hashlib.md5(key).hexdigest()
        _key = base64.urlsafe_b64encode(_key.encode())
        print("ATTENTION: WRITE THIS KEY DOWN. WITHOUT THAT KEY YOUR DATA CANT'T BE DECRYPTED\nYour random working key: ",key.decode())
        command = input("You want to use this key? [y/n]")
        if command == "y":
            path = input("Enter full path to file: ")
            Encrypt(path, 4096, _key)
        Menu("")
    if command == "ck":
        os.system("cls")
        _key = input("Enter key: ")
        _key = hashlib.md5(_key.encode()).hexdigest()
        _key = base64.urlsafe_b64encode(_key.encode())
        input("Press enter key to continue with this key")
        Menu(_key)
    if command == "ef":
        os.system("cls")
        path = input("Enter full path to file: ")
        if _key == "":
            print("no key")
            input("Press any key to continue")
            Menu("")
        Encrypt(path, 4096, _key)
    if command == "df":
        os.system("cls")
        path = input("Enter full path to file: ")
        if _key == "":
            print("no key")
            input("Press enter to continue")
            Menu("")
        Decrypt(path, _key)
    if command == "exit":
        exit()

def WriteKey():
    key = Fernet.generate_key()
    with open(os.getcwd()+"/key", "wb") as key_file:
        key_file.write(key)
    return key
        

def LoadKey():
    try:     
        key = open(os.getcwd()+"/key", "rb").read()
    except IOError:
        print("Can't laod key. Did you create a key with [wk]?")
        input("Press enter to continue")
        Menu("")
    return key

def Encrypt(_filePath, _chunkSize, _key):
    fernet = Fernet(_key)
    try:
        file = open(_filePath, "rb")
    except IOError:
        print("File not found")
        input("Press enter to continue")
        Menu("")
        return
    encryptedFile = open(_filePath+"_ENCRYPTED", "wb")
    fileSize = os.stat(_filePath).st_size
    counter = 0
    print("Your file will be here: " + _filePath + "_ENCRYPTED")
    while True:
        chunk = file.read(_chunkSize)
        encryptedChunk = fernet.encrypt(chunk)
        encryptedFile.write(struct.pack("<I", len(encryptedChunk)))
        encryptedFile.write(encryptedChunk)
        counter += 1
        percent = ((counter * _chunkSize) / fileSize)*100
        print("{:.1f}".format(percent)," %", end = "\r")
        if len(chunk) < _chunkSize:
            print("")
            print("100 %")
            print("Done!")
            input("Press enter to exit")
            exit()

def Decrypt(_filePath, _key):
    fernet = Fernet(_key)
    try:
        encryptedFile = open(_filePath, "rb")
    except IOError:
        print("File not found")
        input("Press any key to continue")
        Menu("")
    _filePath = re.sub("_ENCRYPTED", "", _filePath)
    fileSize = os.stat(_filePath + "_ENCRYPTED").st_size
    if os.path.exists(_filePath):
        decryptedFile = open(_filePath+"_DECRYPTED", "wb")
        print("Your decrypted file will be here: " + _filePath + "_DECRYPTED")
    else:
        print("Your decrypted file will be here: " + _filePath) 
        decryptedFile = open(_filePath, "wb")
    size = 0
    while True:
        dataSize = encryptedFile.read(4)
        if len(dataSize) == 0:
            print("")
            print("100 %")
            print("Done!")
            input("Press enter to exit")
            exit()
        encryptedChunk = encryptedFile.read(struct.unpack("<I", dataSize)[0])
        try:
            decryptedChunk = fernet.decrypt(encryptedChunk)
        except (cryptography.fernet.InvalidToken, TypeError, Error):
            print("Can't decrypt File")
            input("Press enter to exit")
            Menu("")
            break
        size += len(encryptedChunk)
        percent = ((size) / fileSize)*100
        print("{:.1f}".format(percent)," %", end = "\r")
        decryptedFile.write(decryptedChunk)

if __name__ == "__main__":
    print("This is a file en- / decrypter")
    input("Press enter to start")
    key = ""
    Menu(key)