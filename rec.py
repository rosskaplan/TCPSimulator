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
    retval = "0b";
    new_data = t.recbits();
    num = int(new_data[2:10], base = 2);
    if (num == i):
        output = new_data[:8162];
        check = new_data[8162:];
        new_check = str(bin(zlib.adler32((output)))[3:]).zfill(32);
        print(check);
        print(new_check);
        if (new_check == check):
            print('true');
            retval += new_data[2:10];
            print(retval);
            t.sendbits(retval);
            i =  i + 1;
