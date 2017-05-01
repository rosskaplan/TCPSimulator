import pleasetransfer
t=pleasetransfer.pleasetransfer(False)#False for receiver
t.rec_setup()
t.send_setup()
# t.settimeout(10)
while True:
    print t.recbits()
    t.sendbits(bin(123))
