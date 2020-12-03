# README
# Audio Two Factor Authentication
## CIS 428: Introduction to Cryptography final project
## Authors: Andrew Hamann and Cynthia Kar

# Dependencies Used:
- https://numpy.org/install/
- https://pypi.org/project/aubio/
- https://pypi.org/project/PyAudio/
- http://www.portaudio.com/download.html
- https://passlib.readthedocs.io/en/stable/install.html
- https://www.dlitz.net/software/pycrypto/api/current/
- https://github.com/PortAudio/portaudio.git

# System Requirements
- Python3
- Microphone on one device (this device will run client.py. In our development, this was the Raspberry Pi with a microphone attached)
- Speaker on one device (This device will run server.py. In our development, this was a Mac laptop.)

# How to run project
1. Run ` python3 setup.py install ` on both devices to install dependencies on both devices. (On the Raspberry Pi, you may need to run an additional install command. See **Troubleshooting**)
2. Input the IP of the machine playing the sound (the server) in line 14 of server.py and line 14 of client.py. (See **Note** below)
3. Once the IP is entered, run ` python3 server.py ` on the machine that you will be logging in on.
4. Go through login process on the server. Create a username and password, if using the system for the first time.
5. Run ` python3 client.py ` on the client. The two machines will then connect, 3 tones will be played from the server and recorded on the client. If the sound is verified, access will be granted. (There may be a block of warnings from the recording module; you can ignore it.)

## Note:
The server computer is the one you are logging into and the client computer is the second computer listening to the sound. In our use case, a macOS laptop is the server and a Raspberry Pi running Raspbian is the client.

To get your IP, run the following in your terminal
For Windows: "ip config /all"
For macOS: "ipconfig getifaddr en1"
For Raspbian: "hostname -I"

# Troubleshooting:
If pyaudio doesn't work on Raspberry Pi, run the following:
` sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev' `

# Expected Results
## Server (Laptop)
```console
(base) MacBook-Pro:cis428 andrew$ python3 server.py
Welcome to our Program. Would you like to create an account? (y/n)
y
Choose username:
uname
Choose password:
Account successfully created.
Please log in
Enter username:
uname
Choose password:
Login successful. Authenticating through sound...
Generating sound
Starting server and opening socket... Run client.py on other machine
Starting Handshake Protocol...
b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCpO6arZ0benOIiMbCnJYPg+Yx9\neHSCfTPiOXC6QBytdbIuSLr2s/rntuKvAtjWVlXW/G4l8wFKLr70YE2IF5PvNK9d\nfeZudqNraYjvS5CtKTnS/dJIfkokEF0wtTtaP44H9s3HeBpK5A0Jdb3epwPkT3Vh\nSoKyqTfnTb3/TxOEfQIDAQAB\n-----END PUBLIC KEY-----'

Hash of Public Key:
05f8bf0b10dcb5c7dbb04e7aca639b47ab871f84016c853317771ad50cc1f068

Encrypted Session Key and Public Key:
(b'\x92\t]\xfaT\xeafY\xb8k\x88k\xa4\xb4oYc\x8f\xac\xd5\x94)\x8a\xb8\x9a\xa49\xbf\t\x7f\xd0\xa8A!\xcdZ\xf0\xc6\xc84\x07\x8e!\xd6\x8d\x06\x95\xe4\xc9\x8b\x1619v\xb0c\xc6#\xab\xcb\xf5\x0b\x92\xb0\xe6u\xb2\x91\xe9m57\xcfA\xd3?x@\x15\xfd%>>\xb2\x0ba\x81N:\xd4\x02=\xe8\xed\x16\x9d\xdd\xb4\x1f\xbb\xcd\xf6yV\xa5o\xe5\x13\x0e\x8a\xde7\x1a\xf3\x9e\xe6p\xb5\x06\xc8\x1b\xf1d\xf3B\xf3\xaa*',)

Handshake Protocol Complete

Session Key:
701d86733f345fd35bdbe7d19d534269fd1f9c0e631a81a9f406d26665b3ce44
Sending sound sequence
b'Recieved soundSequence'
sleeping play
playing
Response from client: authentic
Permission Access Granted
client disconnected
```

## Client (Raspberry Pi)
```console
pi@raspberrypi:~/cis428 $ python3 client.py
Connecting to server...
Starting Handshake Protocol...
b'YES'
Public key received on server

Encrypted Session Key and Public Key:
 (b'\x92\t]\xfaT\xeafY\xb8k\x88k\xa4\xb4oYc\x8f\xac\xd5\x94)\x8a\xb8\x9a\xa49\xbf\t\x7f\xd0\xa8A!\xcdZ\xf0\xc6\xc84\x07\x8e!\xd6\x8d\x06\x95\xe4\xc9\x8b\x1619v\xb0c\xc6#\xab\xcb\xf5\x0b\x92\xb0\xe6u\xb2\x91\xe9m57\xcfA\xd3?x@\x15\xfd%>>\xb2\x0ba\x81N:\xd4\x02=\xe8\xed\x16\x9d\xdd\xb4\x1f\xbb\xcd\xf6yV\xa5o\xe5\x13\x0e\x8a\xde7\x1a\xf3\x9e\xe6p\xb5\x06\xc8\x1b\xf1d\xf3B\xf3\xaa*',)

Decrypted Session Key:
701d86733f345fd35bdbe7d19d534269fd1f9c0e631a81a9f406d26665b3ce44

Handshake Protocol Complete

Waiting for sound sequence from server
[(600, 2), (1900, 1), (1200, 4)]
...
\* recording to  recording.wav  for  9  seconds
\* done recording
...
pitch length: 769
input [(600, 2), (1900, 1), (1200, 4)]
expected [(600, 0.2857142857142857), (1900, 0.14285714285714285), (1200, 0.5714285714285714)]
averageFrequencies [(601.2462915175454, 0.23276983094928477), (1901.6262463228202, 0.10533159947984395), (1200.346954075636, 0.4408322496749025)]
Response sent: Access Granted
```
