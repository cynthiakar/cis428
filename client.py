import socket
import json
from multiprocessing.connection import Listener
from ast import literal_eval
from soundUtil import SoundUtil
from soundAnalysis import SoundAnalysis
from record import recordWAV
#RASPBERRY PI

# connect to socket and listen for rawWAV pitchList
CLIENT_IP = '192.168.0.19'
SERVER_IP = '192.168.0.5'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('0.0.0.0', 8080)) #localhost
client.connect((SERVER_IP, 8080))
client.send(b'I am CLIENT<br>')
# ser_size = client.recv(4)
# size = json.loads(ser_size.decode())
# print(size)
# client.send(b'Recieved Size<br>')

# ser_rawPitchList = b''
# l = size-47
# while l > 0:
#     d = client.recv(l)
#     l -= len(d)
#     ser_rawPitchList += d
ser_soundSequence = client.recv(88)
soundSequence = json.loads(ser_soundSequence.decode())
client.send(b'Recieved soundSequence<br>')
client.close()
soundSequence = literal_eval(soundSequence)
print(soundSequence)

# record sound
totalDuration = sum([d for _,d in soundSequence])
soundUtil = SoundUtil()
soundUtil.record("recording.wav", totalDuration)
# decrypt package

# get pitchList
soundAnalysis = SoundAnalysis()
recordedPitchList = soundAnalysis.getPitchList("recording.wav")

# testAnalyze for pitch list comparison
soundAnalysis.testAnalyze(soundSequence, recordedPitchList)
# send encrypted verification back to server
