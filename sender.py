import pleasetransfer
import socket
import sys
import hashlib
import zlib
from zlib import adler32
import binascii

t=pleasetransfer.pleasetransfer(True)#true for sender
t.send_setup()
t.rec_setup()
t.settimeout(1)
all_data = "".join(sys.stdin)
x = 1013; #1006 bytes per segment
new_data = [];
full_data = [];
check = [];
output = "";
for i in range(0, (len(all_data)//x)+1):
    output = "";
    adler = "";
    new_data.append(all_data[i:i+x]);
    adler = adler32(new_data[i]);
    check.append(str(int(bin(adler)[3:],base=2)));
    output = str(int(bin(i%128)[2:],base=2)).zfill(2);
    output += check[i];
    output += new_data[i];
    full_data.append(output);

while True:
    try:
        for i in range(0, (len(full_data)//x)+1):
            tosend = "";
            for j in range(0, len(full_data[i])):
                c = full_data[i][j];
                tosend += str(bin(int(ord(c)))[2:]).zfill(8);
            t.sendbits(tosend);
            ack=t.recbits()
            print(ack);
        break
    except socket.timeout:
        pass

# 1. create file
# 2 byte number, 16 byte checksum, 1006 byte other
# 2. write a header function that takes in bits, computes the checksum, and packet number
# 3. append header with bits of length of your choice
# 4. send them, receive the bits
# 5. parse our the header, compare bits to checksum if wrong NAK
# 6. if NAK, we resend it
