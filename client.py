import socket
import json
from multiprocessing.connection import Listener
from ast import literal_eval
from soundUtil import SoundUtil
from record import recordWAV
#RASPBERRY PI

# connect to socket and listen for rawWAV pitchList
CLIENT_IP = '192.168.0.19'
SERVER_IP = '192.168.0.5'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('0.0.0.0', 8080)) #localhost
client.connect((SERVER_IP, 8080))
client.send(b'I am CLIENT<br>')
ser_size = client.recv(4)
size = json.loads(ser_size.decode())
print(size)
client.send(b'Recieved Size<br>')

ser_rawPitchList = b''
l = size-47
while l > 0:
    d = client.recv(l)
    l -= len(d)
    ser_rawPitchList += d
# ser_rawPitchList = client.recv(size)
rawPitchList = json.loads(ser_rawPitchList.decode())
client.send(b'Recieved pitchList<br>')
client.close()
rawPitchList = literal_eval(rawPitchList)
print(rawPitchList)

# record sound
soundUtil = SoundUtil()
soundUtil.record("recording.wav")
# decrypt package

# get pitchList
soundAnalysis = SoundAnalysis()
recordedPitchList = soundAnalysis.getPitchList("recording.wav")

# testAnalyze for pitch list comparison
soundAnalysis.testAnalyze(rawPitchList, recordedPitchList)
# send encrypted verification back to server
