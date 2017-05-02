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

# 1. create file
# 2. write a header function that takes in bits, computes the checksum, and packet number
# 3. append header with bits of length of your choice
# 4. send them, receive the bits
# 5. parse our the header, compare bits to checksum if wrong NAK
# 6. if NAK, we resend it
