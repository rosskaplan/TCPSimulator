import pleasetransfer
import hashlib
from hashlib import md5
import binascii
import sys
import zlib

t=pleasetransfer.pleasetransfer(False)#False for receiver
t.rec_setup()
t.send_setup()
# t.settimeout(10)

x = 1006;
new_data = "";
check = "";
new_check = "";
num = -1;
output = "";
i = 0;
retval = "";

while True:
    retval = "";
    new_data = t.recbits();
    #print new_data[2:10];
    #print new_data[10:42];
    num = int(new_data[2:10], base = 2);
    if (num == i):
        output = new_data[10:8162];
        check = new_data[8162:];
        print(len (output));
        print(len(check));
        new_check = zlib.adler32(output);
        print(new_check);
        print(int(check, base=2));
        if (new_check == check):
            #print(output);
            retval = new_data[0];
            t.sendbits(bin(retval));
            i =  i + 1;
