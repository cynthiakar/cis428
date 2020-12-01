import socket

# MAC LAPTOP

SERVER_IP = '192.168.0.5'
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serv.bind(('0.0.0.0', 8080)) # localhost
serv.bind(('192.168.0.5', 8080))
serv.listen(5)
while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += str(data
        print(from_client)
        conn.send(b'I am SERVER<br>')
    conn.close()
    print('client disconnected')
