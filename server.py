import socket
from soundUtil import SoundUtil
from soundAnalysis import SoundAnalysis
import getpass
from loginsystem import LoginSystem
from security import encrypt_password
import sys

# MAC LAPTOP

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
print(sys.getsizeof(sys.getsizeof(pitchList)))
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
    from_client = ''
    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += str(data)
        print(from_client)
        # conn.send(b''.join(pitchList))
        conn.send(pickle.dumps(sys.getsizeof(pitchList)))
        conn.send(pickle.dumps(pitchList))
    conn.close()
    print('client disconnected')

    # waits/listens for verification

# if verified grant access

# else, generate sound again OR quit
