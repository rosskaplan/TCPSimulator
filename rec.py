import pleasetransfer
import hashlib
from hashlib import md5
import binascii
import sys

t=pleasetransfer.pleasetransfer(False)#False for receiver
t.rec_setup()
t.send_setup()
# t.settimeout(10)

all_data = "".join(sys.stdout);
x = 1006;
m = hashlib.md5()
new_data = []
full_data = []
check = "";
num = "";
output = ""
i = 0;
while True:
	output = "";):
	new_data = str(t.recbits())
	for j in range (0, 1)
		num.append(new_data[j]
	num = int(num);
	if (num == i)
		for j in range (2, 18)
			check.append
		t.sendbits(bin(i))