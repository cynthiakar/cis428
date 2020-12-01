import socket

#RASPBERRY PI

CLIENT_IP = '192.168.0.19'
SERVER_IP = '192.168.0.5'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('0.0.0.0', 8080)) #localhost
client.connect((SERVER_IP, 8080)) 
client.send(b'I am CLIENT<br>')
from_server = client.recv(4096)
client.close()
print(from_server)
