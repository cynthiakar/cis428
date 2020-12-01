import socket

#RASPBERRY PI

CLIENT_IP = '192.168.0.19'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('0.0.0.0', 8080)) #localhost
client.connect((CLIENT_IP, 8080)) #localhost
client.send(b'I am CLIENT<br>')
from_server = client.recv(4096)
client.close()
print(from_server)
