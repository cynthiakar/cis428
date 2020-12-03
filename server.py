from soundUtil import SoundUtil
from soundAnalysis import SoundAnalysis
import getpass
from loginsystem import LoginSystem
from security import encrypt_password
import os, sys, json, socket
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

SERVER_IP = '' # ***** PUT THE IP OF THE MACHINE PLAYING SOUND HERE ****

# MAC LAPTOP
login = LoginSystem()
print("Welcome to our Program. Would you like to create an account? (y/n)")
x = input()
if x == "y":
    print("Choose username:")
    un = input()
    # print("Choose password:")
    # pw = input()
    pw = encrypt_password(getpass.getpass("Choose password:"))
    success = login.createAccount(un, pw)
    while not success:
        print("Username already exists. Try again.")
        print("Choose username:")
        un = input()
        pw = encrypt_password(getpass.getpass("Choose password:"))
        success = login.createAccount(un, pw)
    print("Account successfully created.")
success = False
print("Please log in")
print("Enter username:")
un = input()
while not success:
    # print("Enter password")
    # pw = input()
    pw = getpass.getpass("Choose password:")
    success = login.login(un, pw)
    if success is False:
        print("Try again.")
print("Login successful. Authenticating through sound...")


# generate sound
print("Generating sound")
RECORDEDFILENAME = "recording.wav"
soundUtil = SoundUtil()
soundSequence = soundUtil.generateRandomSound()
soundUtil.createWAV(soundSequence)

soundAnalysis = SoundAnalysis()

# CONNECT TO SOCKET
print("Starting server and opening socket... Run client.py on other machine")

PORT = 8080
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serv.bind(('0.0.0.0', 8080)) # localhost
serv.bind((SERVER_IP, 8080))
serv.listen(5)
while True:
    conn, addr = serv.accept()

    print("Starting Handshake Protocol...")
    # START HANDSHAKE PROTOCOL
    # get publickey from client
    getpbk = conn.recv(2048)

    # conversion of string to key
    server_public_key = RSA.importKey(getpbk)

    # hash received public key string
    hash_object = SHA256.new(getpbk)
    hex_digest = hash_object.hexdigest()

    # send confirmation to client
    if getpbk != "":
        print(getpbk)
        conn.send(b'YES')
        # receive hashed public key
        gethash = conn.recv(1024)
        print ("\nHash of Public Key: \n"+gethash.decode())

    session_key = None
    # check if hashes match
    if hex_digest == gethash.decode():
        # create session key
        key_128 = os.urandom(16)
        # encrypt session key using AES in CTR mode
        encryptor = AES.new(key_128,AES.MODE_CTR,counter = lambda:key_128)
        en_session_key = encryptor.encrypt(key_128)

        # encrypt session key and public key
        E = server_public_key.encrypt(en_session_key,16)
        print("\nEncrypted Session Key and Public Key: \n"+str(E))
        # send encrypted session key and public key
        conn.send(str(E).encode())
        print("\nHandshake Protocol Complete")

        # hashing session key
        en_object = SHA256.new(en_session_key)
        session_key = en_object.hexdigest()

        print("\nSession Key: \n"+session_key)
    # FINISH HANDSHAKE PROTOCOL

    print("Sending sound sequence")
    # SEND EXPECTED SOUND SEQUENCE
    # serialize soundSequence
    message = json.dumps(str(soundSequence))
    # encrypt soundSequence
    key = session_key[:16]
    iv = os.urandom(16)
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(key,AES.MODE_CTR,counter = ctr)
    encrypted_message = iv + cipher.encrypt(message)
    # send encrypted soundSequence
    conn.send(encrypted_message)

    # RECEIVE CONFIRMATION
    data = conn.recv(4096)
    print(data)

    # PLAY SOUND
    if data == b'Recieved soundSequence':
         soundUtil.play()

    # RECEIVE ENCRYPTED AUTHENTICATION RESPONSE
    data = conn.recv(4096)

    # decrypt message
    key = session_key[:16]
    iv = data[:16]
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(key,AES.MODE_CTR,counter = ctr)
    decrypted_message = cipher.decrypt(data[16:])
    # verify signature with public key
    message = decrypted_message[:14]
    signature = decrypted_message[14:]
    h = SHA256.new(message)
    verifier = PKCS1_v1_5.new(server_public_key)
    if verifier.verify(h, signature):
        print("Response from client: authentic")
        print("Permission", message.decode())
    else:
        print("Response from client: not authentic")

    # close connection
    conn.close()
    print('client disconnected')
