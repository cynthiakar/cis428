import audioWritePlay
import compareWAV
import aubio
from loginsystem import LoginSystem
from security import encrypt_password

def soundProtocol():
    #generate sound and save
    sounds = [(400,2),(600,1),(1000,5)]

    totalDuration = 0
    for (_,d)in sounds:
        totalDuration += d

    if (totalDuration != 0):
        expectedFD = [(f, (d/totalDuration)) for (f,d) in sounds]

    audioWritePlay.writeWAVFile(sounds)

    #analyze sound
    analysis = compareWAV.compareWav("sound.wav")

    results = []
    for i in range(len(expectedFD)):
        results.append((abs(expectedFD[i][0] - analysis[i][0]),abs(expectedFD[i][1] - analysis[i][1])))

    #print(expectedFD)
    #print(analysis)
    print(results)

def loginProtocol():
    login = LoginSystem()
    print("Welcome to our Program. Would you like to create an account? (y/n)")
    x = input()
    if x == "y":
        print("Choose username:")
        un = input()
        print("Choose password:")
        pw = encrypt_password(input())
        while not login.createAccount(un, pw):
            print("Username already exists. Try again.")
        print("Account successfully created.")
    success = False
    print("Please log in")
    print("Enter username:")
    un = input()
    while not success:
        print("Enter password")
        pw = input()
        success = login.login(un, pw)
        if success is False:
            print("Try again.")
    print("Login successful")


if __name__ == "__main__":
    loginProtocol()
    # soundProtocol()
