import socket
from soundUtil import SoundUtil
from soundAnalysis import SoundAnalysis
import getpass
from loginsystem import LoginSystem
from security import encrypt_password
import sys
import json

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
print("Login successful")


# generate sound
RECORDEDFILENAME = "recording.wav"
soundUtil = SoundUtil()
soundSequence = soundUtil.generateRandomSound()
soundUtil.createWAV(soundSequence)

soundAnalysis = SoundAnalysis()
# send encrypted package to Pi including rawWAVFile, digital signature?
    # create pitch list
pitchList = soundAnalysis.getPitchList(soundUtil.soundFile)
print(sys.getsizeof(pitchList))
print(sys.getsizeof(str(pitchList)))
print(len(pitchList))
    # encrypt

    # socket and send
CLIENT_IP = '192.168.0.19'
SERVER_IP = '192.168.0.5'
PORT = 8080
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serv.bind(('0.0.0.0', 8080)) # localhost
serv.bind((SERVER_IP, 8080))
serv.listen(5)
while True:
    conn, addr = serv.accept()
    # receive "I am CLIENT"
    data = conn.recv(4096)
    print(data)

    # # send array length
    # conn.send(json.dumps(sys.getsizeof(str(soundSequence))).encode())
    #
    # # receive confirmation
    # data = conn.recv(4096)
    # print(data)

    # send pitchList
    conn.send(json.dumps(str(soundSequence)).encode())

    # receive confirmation
    data = conn.recv(4096)
    print(data)

    if data == b'Recieved soundSequence<br>':
        break

    # close connection
    conn.close()
    print('client disconnected')

# play sound
soundUtil.play()

# waits/listens for verification

# if verified grant access

# else, generate sound again OR quit
