import socket
from random import randint
import array

class pleasetransfer(object):

    def __init__(self, sender):
        self.ip = "127.0.0.1"
        self.ss = None
        self.sr = None
        self.swap = None
        self.swap_bool = False
        if sender:
            self.sendport=50005
            self.recport=50006
        else:
            self.sendport=50006
            self.recport=50005

    def send_setup(self):
        self.ss = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def send(self, bits):
        bitstring=bits[2:]
        # bitarray=array.array('i', (0 for i in range ( 0, len(bitstring)/8)))
        barray=bytearray()
        for n in xrange(0,len(bitstring)/8):
            barray.append(int(bitstring[(n*8):((n*8)+8)],2))
        self.ss.sendto(barray, (self.ip, self.sendport))

    def rec_setup(self):
        self.sr = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sr.bind((self.ip, self.recport))
    def rec(self):
        while True:
            data, addr = self.sr.recvfrom(1024) # buffer size is 1024 bytes
            barray=bytearray(data)
            bitstring = "0b"
            for n in xrange(0,len(barray)):
                bitstring+=(bin(barray[n])[2:])
            return bitstring

    def sendbits(self, bits):
        print self.swap_bool
        # if self.swap_bool==True
        #     self.send(self.swap)
        #     self.swap=None
        #     self.swap_bool=False
        r=randint(0,5000)
        s=randint(0,5000)
        d=randint(0,5000)
        if r<=10:
            # print bits
            bitlist=list(bits)
            for n in xrange(0,randint(0,len(bitlist)/3)):
                bitlist[randint(3,len(bitlist))-1]=str(randint(0,1))
            bits=''.join(bitlist)
            # print bits
        if s<10:
            self.swap_bool=True
            self.swap=bits
            return
        if d<=10:
            return
        self.send(bits)

    def recbits(self):
        return self.rec()

    def settimeout(self, time):
        self.ss.settimeout(time)
        self.sr.settimeout(time)
