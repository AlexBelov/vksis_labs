import pipes
import time
import random

t = pipes.Template()

def send_packet_data():
    str_new = ""
    str = 'e\r\x0c\x06h\xff\x9allo\x1d'
    dst = random.randint(14,255)
    str_new += str[0]
    str_new += chr(dst)
    for i in range(2, len(str)-2):
        str_new += str[i]
    return str_new, dst

while(True):
    f = t.open('pipefile', 'w')
    option = random.randint(1,4)
    if option == 1:
        str, addr = send_packet_data()
        print 'Send packet to wrong address {}'.format(addr)
    else:
        size = random.randint(1,20)
        str = ""
        for i in range(size):
            str += chr(random.randint(0,255))
    print str
    f.write(str)
    f.close()
    time.sleep(1)