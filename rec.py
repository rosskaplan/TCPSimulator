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
    print new_data[2:10];
    num = int(new_data[0]);
    #print num;
    if (num == i):
        output = new_data[6:];
        #print(output);
        check = new_data[2:4];
        #print check;
        new_check = zlib.adler32(output);
        if (new_check == check):
            #print(output);
            retval = new_data[0];
            t.sendbits(bin(retval));
