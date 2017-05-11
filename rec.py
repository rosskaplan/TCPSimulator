import pleasetransfer
import hashlib
import socket
from hashlib import md5
import binascii
from binascii import b2a_uu
import sys
import zlib

t=pleasetransfer.pleasetransfer(False)
t.rec_setup()
t.send_setup()
t.settimeout(0.01)

windowsize = 5;
x = 1019;
new_data = "";
check = "";
new_check = "";
num = -1;
check_output = "";
i = 0;
retval = "";
flag_main = 0;
output = [];

while True:
    retval = "0b";
    flag_main = 0;
    
    i = i % 100;
    for j in range (0, windowsize):
        counter = 0;
        flag = 0;
        new_data = "";
        while True:
            counter += 1;
            try:
                new_data = t.recbits();
            except socket.timeout:
                flag = 2;
                break;
            if (new_data != ""):
                flag = 1;
                break;
            elif (counter > 1000):
                flag = 2;
                break;

        if (flag == 1):
            if (flag_main == 0):
                num = int(new_data[2:10], base = 2);
                if (num == i + j):
                    if (len(new_data) < 8192):
                        check_output = new_data[:len(new_data) - 32];
                        check = new_data[len(new_data) - 32:];
                        sys.stderr.write(check + "\n");
                    else:
                        check_output = new_data[:8162];
                        check = new_data[8162:];
                    new_check = str(bin(zlib.adler32((check_output)))[3:]).zfill(32);
                    output.append(check_output[10:]);
                    if (new_check == check):
                        if (len(new_data) < 8192):
                            sys.stderr.write("working\n");
                            for k in range (0, j + 1):
                                out = "".join((chr(int(output[k][loop:loop+8], 2)) for loop in range(0, len(output[k]), 8)))
                                sys.stdout.write(out);
                            sys.exit(0);
                        if (j == windowsize - 1):
                            i = i + windowsize;
                            for k in range (0, windowsize):
                                out = "".join((chr(int(output[k][loop:loop+8], 2)) for loop in range(0, len(output[k]), 8)))
                                sys.stdout.write(out);
                                allzeros = '00110000'*(len(output[k])/8);
                            output = [];
                            retval += str(bin(i)[2:]).zfill(8);
                            flag_main = 1;
                    else:
                        retval += (str(bin(i)[2:]).zfill(8));
                        flag_main = 2;
                        output = [];
                else:
                    retval += (str(bin(i)[2:]).zfill(8));
                    flag_main = 2;
                    output = [];
        elif (flag == 2):
            retval += (str(bin(i)[2:]).zfill(8));
            flag_main = 2;
            output = [];
            break;

    if flag != 2:
        t.sendbits(retval);
