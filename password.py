from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

print('enter username:')
username = input()

print('enter password:')
password = input()

key = get_random_bytes(32) 
obj = AES.new(key, AES.MODE_CFB, 'This is an IV456')
message = "The answer is no"
ciphertext = obj.encrypt(password)
print('encrypted password:',ciphertext)

obj2 = AES.new(key, AES.MODE_CFB, 'This is an IV456')
decrypttext = obj2.decrypt(ciphertext)
print('decrypted password', decrypttext)

