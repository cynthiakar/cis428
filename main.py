import aubio
from loginsystem import LoginSystem
from security import encrypt_password
from soundUtil import SoundUtil
from soundAnalysis import SoundAnalysis
import os
import struct
import getpass
from multiprocessing import Process
import subprocess
import time

def generateRandomSound():
    x1 = struct.unpack('I', os.urandom(4))[0]
    y1 = struct.unpack('I', os.urandom(4))[0]
    z1 = struct.unpack('I', os.urandom(4))[0]
    x2 = struct.unpack('I', os.urandom(4))[0]
    y2 = struct.unpack('I', os.urandom(4))[0]
    z2 = struct.unpack('I', os.urandom(4))[0]
    return [((x1%50+1)*100,x2%4+1), ((y1%50+1)*100,y2%4+1), ((z1%50+1)*100,z2%4+1)]

def soundProtocol(filename, expectedSound):
    soundUtil = SoundUtil(filename, expectedSound)
    soundAnalysis = SoundAnalysis(filename, expectedSound)
    soundUtil.write()

    # p1 = Process(target=record,args=(i,))
    # p2 = Process(target=play,args=(i,))
    p1 = Process(target=soundUtil.record)
    p2 = Process(target=soundUtil.play)
    p1.start()
    # time.sleep(200)
    p2.start()
    p2.join()
    p1.join()
    print("retrieving files from raspberry pi")
    subprocess.run("scp pi@192.168.0.19:/home/pi/cis428/"+filename+" /Users/andrew/School/senior_fall/Cryptography/Audio\ Security\ Project/cis428", shell=True)

    print(soundAnalysis.testAnalyze(expectedSound,filename))

def loginProtocol():
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

if __name__ == "__main__":
    # loginProtocol()
    soundProtocol("recording.wav", generateRandomSound())
