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

# MAC LAPTOP

# generate sound
RECORDEDFILENAME = "recording.wav"
soundUtil = SoundUtil()
soundSequence = soundUtil.generateRandomSound()
soundUtil.createWAV(soundSequence)

soundAnalysis = SoundAnalysis()
# CONNECT TO SOCKET
CLIENT_IP = '192.168.0.19' # raspberry pi
SERVER_IP = '192.168.0.5' # mac laptop
PORT = 8080
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080)) # localhost
# serv.bind((SERVER_IP, 8080))
serv.listen(5)
while True:
    conn, addr = serv.accept()

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
        print ("\n-----HASH OF PUBLIC KEY----- \n"+gethash.decode())

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
        print("\n-----ENCRYPTED PUBLIC KEY AND SESSION KEY-----\n"+str(E))
        # send encrypted session key and public key
        conn.send(str(E).encode())
        print("\n-----HANDSHAKE COMPLETE-----")

        # hashing session key
        en_object = SHA256.new(en_session_key)
        session_key = en_object.hexdigest()

        print("\n-----SESSION KEY-----\n"+session_key)
    # FINISH HANDSHAKE PROTOCOL

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
    # if data == b'Recieved soundSequence':
    #     soundUtil.play()

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
        print("authentic")
        print(message.decode())
    else:
        print("not authentic")

    # close connection
    conn.close()
    print('client disconnected')
