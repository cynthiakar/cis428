import socket
import json
from multiprocessing.connection import Listener

#RASPBERRY PI

# connect to socket and listen for rawWAV pitchList
# record sound
# decrypt package
# compareWAV2 for pitchList
# testAnalyze2 for pitch list comparison
# send encrypted verification back to server

CLIENT_IP = '192.168.0.19'
SERVER_IP = '192.168.0.5'


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('0.0.0.0', 8080)) #localhost
client.connect((SERVER_IP, 8080))
client.send(b'I am CLIENT<br>')
ser_size = client.recv(28)
print(ser_size)
size = json.loads(ser_size.decode())
print(size)
client.send(b'Recieved Size<br>')

ser_rawPitchList = b''
l = size
while l > 0:
    d = client.recv(l)
    l -= len(d)
    ser_rawPitchList += d
# ser_rawPitchList = client.recv(size)
rawPitchList = json.loads(ser_rawPitchList.decode())
client.send(b'Recieved pitchList<br>')
client.close()
print(rawPitchList)
