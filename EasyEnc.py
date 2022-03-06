import os, re, struct, threading, hashlib, base64
from tkinter.ttk import Progressbar
from cryptography.fernet import Fernet
from cryptography import *
import cryptography
from binascii import Error
from tkinter import *
from tkinter import filedialog
from turtle import Turtle

workingKey = ""
workingFilePaht = ""
progressValue = 0

########################Controll&Functionality-Par##########################
def loadKey():
    global workingKey 
    workingKey = LoadKey()
    if workingKey == "":
        return
    key = workingKey.decode()
    updateTextBox("Key loaded. And ready to use.\nKey-Value: " + key)
    updateWorkingKey(key)

def writeKey():
    if workingKey == "":
        updateTextBox("You have to set a working key.\n - Enter a custom key and click on \"Set Custom key\"\n - Or create a random key by clicking on \"Random Key\"")
        return
    WriteKey(workingKey)

def loadFile():
    global workingFilePaht
    workingFilePaht = filedialog.askopenfilename()
    fileNameText.delete(0.0, END)
    fileNameText.insert(END, workingFilePaht)

def encryptFile():
    thread = threading.Thread(target=Encrypt(workingFilePaht, 4096, workingKey))
    thread.daemon = Turtle
    thread.start()
    thread.join()
    return None

def updateTextBox(_text):
    outputText.delete(0.0, END)
    outputText.insert(END, _text)

def updateWorkingKey(_keyValue):
    workingKeyText.delete(0.0, END)
    workingKeyText.insert(END, "Working-Key: " + _keyValue)

def progress():
    progressBar['value'] = progressValue
    window.update_idletasks()

def decryptFile():
    thread = threading.Thread(target=Decrypt(workingFilePaht, workingKey))
    thread.daemon = Turtle
    thread.start()
    thread.join()
    return None

def randomKey():
    key = Fernet.generate_key()
    _key = hashlib.md5(key).hexdigest()
    _key = base64.urlsafe_b64encode(_key.encode())
    updateTextBox("WARNING: WRITE THIS KEY DOWN IT'S IMPOSSIBLE TO DECRYPT THE DATA WITHOUT!\nYour random generated Key is ready to use.\nKey-Value: " + key.decode())
    updateWorkingKey(key.decode())
    global workingKey
    workingKey = _key
    return None

def customKey():
    enteredText = keyEntry.get()
    _key = hashlib.md5(enteredText.encode()).hexdigest()
    _key = base64.urlsafe_b64encode(_key.encode())
    global workingKey
    workingKey = _key
    updateTextBox("Your current key is: " + enteredText)
    updateWorkingKey(enteredText)


########################GUI-PART########################
window = Tk()
window.title("EasyEnc")
window.configure(background='#98e1fa')

Label(window, text="EASY ENCRYPTION AND DECRYPTION", bg="#98e1fa", fg="black", font="Lemon 24 bold").grid(row=0, columnspan=7)

Button(window, text="Load Key", width=14, command=loadKey).grid(row=1, column=0, sticky=W,padx=10, pady=5)
Button(window, text="Random Key", width=14, command=randomKey).grid(row=1, column=1, sticky=W,padx=10, pady=5)
Button(window, text="Write Key", width=9, command=writeKey).grid(row=1, column=5, sticky=E,padx=10, pady=5)
Label (window, text="Key settings:", bg="#98e1fa", font="none 12 bold").grid(row=2, column=0, sticky=W,padx=10, pady=5)
workingKeyText = Text(window, width=60, height=1, wrap=WORD, background="#98e1fa")
workingKeyText.grid(row=2, column=1, columnspan=6, sticky=W, padx=10, pady=5)
workingKeyText.insert(END, "Working-Key: no key loaded")
keyEntry = Entry(window, width=80, bg="#98e1fa")
keyEntry.grid(row=3, column=1, columnspan=6, sticky=W, padx=10, pady=5)
Button(window, text="Set Custom Key", width=14, command=customKey).grid(row=3, column=0, sticky=W ,padx=10, pady=5)
Button(window, text="Load File", width=14, command=loadFile).grid(row=4, column=0,sticky=W ,padx=10, pady=5)
fileNameText = Text(window, width=60, height=1, wrap=WORD, bg="#98e1fa")
fileNameText.grid(row=4, column=1, columnspan=6, sticky=W, padx=10, pady=5)
Label (window, text="En- / Decryption:", bg="#98e1fa", font="none 12 bold").grid(row=5, column=0, sticky=W, padx=10, pady=5)
Button(window, text="Encrypt File", width=12, command=encryptFile).grid(row=6, column=0, sticky=W, padx=10, pady=6)
Button(window, text="Decrypt File", width=12, command=decryptFile).grid(row=6, column=1, sticky=W, padx=10, pady=5)

progressBar = Progressbar(window, orient='horizontal', mode='determinate', length=640)
progressBar.grid(row=7,columnspan=6,padx=10, pady=20)
outputText = Text(window, width=80, height=6, wrap=WORD, background="#98e1fa")
outputText.grid(row=8, column=0, columnspan=8, sticky=W, padx=10, pady=20)
outputText.insert(END, "ATTENTION! SOME RULES BEFORE USING THIS TOOL:\n - Use this on your own risk. If you lost your key I can't help you.\n - If you write a key it overwrites and becomes your default key.\n - How to write a key? Press the \"Write Key\"-Button\n - That writes your current working key do disk")

###################CRYPTO-PART####################

def WriteKey(_key):
    path = os.getcwd()+"/key"
    updateTextBox("Overwriting key @" +path + "\nIt is also your new default key")
    with open(path, "wb") as keyFile:
        keyFile.write(_key)
    return _key

def LoadKey():
    try:     
        key = open(os.getcwd()+"/key", "rb").read()
    except IOError:
        updateTextBox("Can't laod key. Did you create a key with [write key]?")
        return ""
    return key

def Encrypt(_filePath, _chunkSize, _key):
    global progressValue
    fernet = Fernet(_key)
    try:
        file = open(_filePath, "rb")
    except IOError:
        updateTextBox("File not found")
        return
    encryptedFile = open(_filePath+"_ENCRYPTED", "wb")
    fileSize = os.stat(_filePath).st_size
    counter = 0
    updateTextBox("Your encrypted file will be here: " + _filePath + "_ENCRYPTED")
    while True:
        chunk = file.read(_chunkSize)
        encryptedChunk = fernet.encrypt(chunk)
        encryptedFile.write(struct.pack("<I", len(encryptedChunk)))
        encryptedFile.write(encryptedChunk)
        counter += 1
        percent = ((counter * _chunkSize) / fileSize)*100
        progressValue = float("{:.1f}".format(percent))
        progress()
        if len(chunk) < _chunkSize:
            progressValue = 0
            progress()
            updateTextBox("Encryption done!\nYour encrypted file is here: " + _filePath + "_ENCRYPTED")
            return
            exit()

def Decrypt(_filePath, _key):
    global progressValue
    fernet = Fernet(_key)
    try:
        encryptedFile = open(_filePath, "rb")
    except IOError:
        updateTextBox("File not found")
        return
    _filePath = re.sub("_ENCRYPTED", "", _filePath)
    fileSize = os.stat(_filePath + "_ENCRYPTED").st_size
    if os.path.exists(_filePath):
        decryptedFile = open(_filePath+"_DECRYPTED", "wb")
        updateTextBox("Your decrypted file will be here: " + _filePath + "_DECRYPTED")
    else:
        updateTextBox("Your decrypted file will be here: " + _filePath) 
        decryptedFile = open(_filePath, "wb")
    size = 0
    while True:
        dataSize = encryptedFile.read(4)
        if len(dataSize) == 0:
            progressValue = 0
            progress()
            if os.path.exists(_filePath):
                updateTextBox("Your decrypted file is here: " + _filePath + "_DECRYPTED")
            else:
                updateTextBox("Your decrypted file is here: " + _filePath) 
            return
        encryptedChunk = encryptedFile.read(struct.unpack("<I", dataSize)[0])
        try:
            decryptedChunk = fernet.decrypt(encryptedChunk)
        except (cryptography.fernet.InvalidToken, TypeError, Error):
            updateTextBox("Can't decrypt File")
            return
        size += len(encryptedChunk)
        percent = ((size) / fileSize)*100
        progressValue = float("{:.1f}".format(percent))
        progress()
        decryptedFile.write(decryptedChunk)

window.mainloop()