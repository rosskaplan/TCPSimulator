import pleasetransfer
import socket
import sys
import hashlib
from hashlib import md5
import binascii

t=pleasetransfer.pleasetransfer(True)#true for sender
t.send_setup()
t.rec_setup()
t.settimeout(1)
all_data = "".join(sys.stdin)
x = 1006; #1006 bytes per segment
m = hashlib.md5();
new_data = [];
full_data = [];
check = [];
output = "";
for i in range(0, (len(all_data)//x)+1):
    output = "";
    new_data.append(all_data[i:i+x]);
    m.update(new_data[i]);
    check.append(m.digest());
    output = str(int(bin(i%65536)[2:],base=2)).zfill(2);
    output += check[i];
    output += new_data[i];
    full_data.append(output);

while True:
    try:
        for i in range(0, (len(all_data)//x)+1):
            print len(full_data[i]);
            print full_data[i];
            t.sendbits(bin(full_data[i]));
            ack=t.recbits()
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
