import socket
import pickle
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

PORT = 8080
server_sock = Listener((SERVER_IP, PORT))
conn = server_sock.accept()

conn.send(b'I am LISTENER<br>')
unpickled_data = conn.recv()
conn.close()
print(unpickled_data)
print(pickle.loads(unpickled_data))

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # client.connect(('0.0.0.0', 8080)) #localhost
# client.connect((SERVER_IP, 8080))
# client.send(b'I am CLIENT<br>')
# from_server = client.recv(8192)
# client.close()
# print(pickle.loads(from_server))
