import pleasetransfer
import hashlib
import socket
from hashlib import md5
import binascii
from binascii import b2a_uu
import sys
import zlib

t=pleasetransfer.pleasetransfer(False)#False for receiver
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
                #print("socket timeout");
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
                        check_output = new_data[:len(new_data) - 31];
                        check = new_data[len(new_data) - 31:];
                        exit(0);
                    check_output = new_data[:8162];
                    check = new_data[8162:];
                    new_check = str(bin(zlib.adler32((check_output)))[3:]).zfill(32);
                    output.append(check_output[10:]);
                    if (new_check == check):
                        #print('true');
                        if (j == windowsize - 1):
                            i = i + windowsize;
                            #print("We will print the last 5 receives here")
                            for k in range (0, windowsize):
                                out = "".join((chr(int(output[k][loop:loop+8], 2)) for loop in range(0, len(output[k]), 8)))
                                allzeros = '0'*x;
                                if (output[k] != allzeros):
                                    sys.stdout.write(out)
                            output = [];
                            #print(i);
                            retval += str(bin(i)[2:]).zfill(8);
                            flag_main = 1;
                    else:
                        #print('false');
                        retval += (str(bin(i)[2:]).zfill(8));
                        flag_main = 2;
                        output = [];
                else:
                    #print('false 2');
                    retval += (str(bin(i)[2:]).zfill(8));
                    #print "false 2" + str(retval);
                    flag_main = 2;
                    output = [];
        elif (flag == 2):
            #print('no rec');
            retval += (str(bin(i)[2:]).zfill(8));
            #print "no rec: " + str(retval);
            flag_main = 2;
            output = [];
            break;

    #print "retval: " + retval;
    if flag != 2:
        t.sendbits(retval);
