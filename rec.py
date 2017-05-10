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

windowsize = 5;
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

    for j in range (0, windowsize):
        new_data = t.recbits();
        num = int(new_data[2:10], base = 2);
        if (num == i + j):
            output = new_data[:8162];
            check = new_data[8162:];
            new_check = str(bin(zlib.adler32((output)))[3:]).zfill(32);
            if (new_check == check):
                print('true');
                if (j == 4):
                    i = i + windowsize;
                    print("We will print the last 5 receives here")
            else:
                print('false');
                retval += (str(bin(i - 1)[3:]).zfill(8));
                print (retval);
                break;
        else:
            print('false 2');
            retval += (str(bin(i - 1)[3:]).zfill(8));
            print (retval);
            break;
