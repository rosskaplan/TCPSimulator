import pleasetransfer
import socket

t=pleasetransfer.pleasetransfer(True)#true for sender
t.send_setup()
t.rec_setup()
t.settimeout(1)
while True:
    try:
        t.sendbits(bin(2344))
        ack=t.recbits()
        print ack
        break
    except socket.timeout:
        pass
