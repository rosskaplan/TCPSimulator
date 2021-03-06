import pleasetransfer
import socket
import sys
import hashlib
import zlib
from zlib import adler32
import binascii
import time

t=pleasetransfer.pleasetransfer(True)
t.send_setup()
t.rec_setup()
t.settimeout(0.01)
all_data = "".join(sys.stdin)
x = 1019;
windowsize = 5;
new_data = [];
full_data = [];
check = [];
output = "";

start_time = time.time();

for i in range(0, (len(all_data)//x)+1):
    output = "";
    new_data.append(all_data[i*x:i*x+x]);
    output = str(bin(int(i%100))[2:]).zfill(8);
    output += new_data[i];
    full_data.append(output);



counter = 0;
flag = 0;
ack = "";

retnum = 0;

while True:
    try:
        i = 0;
        while i < len(full_data):
            if (i == len(full_data) - 1):
                print ("--- %s seconds ---" % (time.time() - start_time));
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
            if (i == len(full_data) - 1):
                sys.exit(0);
                while True:
                    try:
                        ack=t.recbits();
                    except socket.timeout:
                        flag = 2;
                        break;
                    if ack != "":
                        flag = 1;
                        break;
                    if counter > 1000: 
                        flag = 2;
                        break;
            if ((i%100) % windowsize == (windowsize - 1)):
                counter = 0;
                flag = 0;
                ack = "";
                while True:
                    counter += 1;
                    try:
                        ack=t.recbits();
                    except socket.timeout:
                        flag = 2;
                        break;
                    if ack != "":
                        flag = 1;
                        break;
                    if counter > 1000: 
                        flag = 2;
                        break;
                if flag == 1: 
                    retnum = int(ack[2:10], base=2);
                    if (retnum-1) != (i%100):
                        if (retnum + 99) != (i%100):
                            i -= (windowsize - 1);
                            continue;
                elif flag == 2:
                    i -= (windowsize - 1);
                    continue;
            i += 1;
        break;
    except socket.timeout:
        pass
