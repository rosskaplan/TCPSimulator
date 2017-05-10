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
x = 1019;
windowsize = 5;
new_data = [];
full_data = [];
check = [];
output = "";
for i in range(0, (len(all_data)//x)+1):
    output = "";
    new_data.append(all_data[i:i+x]);
    output = str(bin(int(i%100))[2:]).zfill(8);
    output += new_data[i];
    full_data.append(output);

retnum = 0;
while True:
    try:
        i = 0;
        while i < len(full_data):
            print("itop: " + str(i));
            adler = "";
            tosend = "0b";
            for j in range(0, len(full_data[i])):
                if j < 8:
                    tosend += full_data[i][j];
                else: 
                    c = full_data[i][j];
                    tosend += str(bin(ord(c))[2:]).zfill(8);
            adler = adler32(tosend);
            tosend += str(bin(adler)[3:]).zfill(32);
            t.sendbits(tosend);
            if ((i%100) % windowsize == 4):
                ack=t.recbits();
                retnum = int(ack[2:10], base=2);
                print "ret: " + str(retnum)
                print "i: " + str(i);
                if (retnum-1) != (i%100):
                    print "bit errors"
                    i -= 4;
                    continue;
            i += 1;
        break;
    except socket.timeout:
        pass
