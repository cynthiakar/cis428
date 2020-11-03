import os
import struct

x1 = struct.unpack('I', os.urandom(4))[0]
y1 = struct.unpack('I', os.urandom(4))[0]
z1 = struct.unpack('I', os.urandom(4))[0]
x2 = struct.unpack('I', os.urandom(4))[0]
y2 = struct.unpack('I', os.urandom(4))[0]
z2 = struct.unpack('I', os.urandom(4))[0]
print([(x1%1000,x2%10), (y1%1000,y2%10), (z1%1000,z2%10)])