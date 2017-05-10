import pleasetransfer
import hashlib
from hashlib import md5
import binascii
import sys
import zlib

t=pleasetransfer.pleasetransfer(False)#False for receiver
t.rec_setup()
t.send_setup()
t.settimeout(10)

windowsize = 5;
x = 1019;
new_data = "";
check = "";
new_check = "";
num = -1;
output = "";
i = 0;
retval = "";

while True:
    retval = "0b";
    
    i = i % 100;
    for j in range (0, windowsize):
        counter = 0;
        flag = 0;
        new_data = "";
        while (true):
            counter += 1;
            new_data = t.recbits();
            if (new_data != ""):
                flag = 1;
                break;
            elif (counter > 1000):
                flag = 2;
                break;

        if (flag == 1):
            num = int(new_data[2:10], base = 2);
            print "num: " + str(num) + ';' + " i: " + str(i) + ';' + " j: " + str(j);
            if (num == i + j):
                output = new_data[:8162];
                check = new_data[8162:];
                new_check = str(bin(zlib.adler32((output)))[3:]).zfill(32);
                if (new_check == check):
                    print('true');
                    if (j == 4):
                        i = i + windowsize;
                        print("We will print the last 5 receives here")
                        print(i);
                        retval += str(bin(i)[2:]).zfill(8);
                else:
                    print('false');
                    i = i - (j%windowsize) + 1;
                    retval += (str(bin(i)[2:]).zfill(8));
                    break;
            else:
                print('false 2');
                retval += (str(bin(i - 1)[2:]).zfill(8));
                print "false 2" + str(retval);
                i = i - (j%windowsize) + 1;
                break;
        elif (flag == 2):
            print('no rec');
            retval += (str(bin(i - 1)[2:]).zfill(8));
            print "no rec: " + str(retval);
            i = i - (j%windowsize) + 1;
            break;

    print retval;
    t.sendbits(retval);
