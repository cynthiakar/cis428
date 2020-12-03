import os, socket, json
from multiprocessing.connection import Listener
from ast import literal_eval
from soundUtil import SoundUtil
from soundAnalysis import SoundAnalysis
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

#RASPBERRY PI

# CONNECT TO SOCKET
CLIENT_IP = '192.168.0.19' # raspberry pi
SERVER_IP = '192.168.0.5' # mac laptop

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 8080)) #localhost
# client.connect((SERVER_IP, 8080))

# START HANDSHAKE PROTOCOL
# public key and private key generation
random_generator = Random.new().read
key = RSA.generate(1024,random_generator)
public = key.publickey().exportKey()
private = key.exportKey()

# hash public key
hash_object = SHA256.new(public)
hex_digest = hash_object.hexdigest()

# send unhashed public key
client.send(public)

# receive confirmation
conf = client.recv(3)
print(conf)
session_key = None
if conf == b'YES':
	print("public key received")
	# send hashed public key
	client.send(hex_digest.encode())

	# receive encrypted session key and public key
	msg = client.recv(1024).decode()
	en = eval(msg)

	# decrypt using RSA key
	decrypt = key.decrypt(en)
	# hashing session key
	en_object = SHA256.new(decrypt)
	en_digest = en_object.hexdigest()

	session_key = en_digest

	print("\n-----ENCRYPTED PUBLIC KEY AND SESSION KEY FROM SERVER-----")
	print(msg)
	print("\n-----DECRYPTED SESSION KEY-----")
	print(session_key)
	print("\n-----HANDSHAKE COMPLETE-----\n")
# FINISH HANDSHAKE PROTOCOL

# RECEIVE ENCRYPTED SOUND SEQUENCE
en_soundSequence = client.recv(1024)
# decrypt soundSequence using session key
key = session_key[:16]
iv = en_soundSequence[:16]
ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
cipher = AES.new(key,AES.MODE_CTR,counter = ctr)
decrypted_message = cipher.decrypt(en_soundSequence[16:])
# deserialize soundsequence
soundSequence = json.loads(decrypted_message.decode())
client.send(b'Recieved soundSequence')
# load as array of floats
soundSequence = literal_eval(soundSequence)
print(soundSequence)

# RECORD SOUND
totalDuration = sum([d for _,d in soundSequence])
soundUtil = SoundUtil()
soundUtil.record("recording.wav", totalDuration)
# decrypt package

# GET PITCH LIST
soundAnalysis = SoundAnalysis()
recordedPitchList = soundAnalysis.getPitchList("recording.wav")

# ANALYZE SOUNDS USING PITCH LIST COMPARISON
if (soundAnalysis.testAnalyze(soundSequence, recordedPitchList)):
	response = "Access Granted"
else:
	response = "Access Denied!"

# SEND ENCRYPTED AUTHENTICATION RESPONSE

# create digital signature
h = SHA256.new(response.encode())
# sign using private key
signer = PKCS1_v1_5.new(RSA.importKey(private))
signature = signer.sign(h)
message = response.encode() + signature
# encrypt message
key = session_key[:16]
iv = os.urandom(16)
ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
cipher = AES.new(key,AES.MODE_CTR,counter = ctr)
encrypted_message = iv + cipher.encrypt(message)
# send encrypted message
client.send(encrypted_message)
print("Response sent:", response)

client.close()
