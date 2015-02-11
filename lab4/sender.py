import pipes
import os
import sys
import logging
import time
import random

logging.basicConfig(filename='info.log',level=logging.INFO)
logger = logging.getLogger("Sender")

flags = [0x65, 0xFF]
t = pipes.Template()

if len(sys.argv) > 1:
    my_addr = int(sys.argv[1])
else:
    my_addr = 12

if len(sys.argv) > 2:
    dest_addr = int(sys.argv[2])
else:
    dest_addr = 13

def send_encoded(encoded):
    f = t.open('pipefile', 'w')
    f.write(encoded)
    f.close()

def send_until(times):
    while times > 0:
        f = t.open('pipefile', 'r')
        channel = f.read().rstrip('\n')
        f.close()

        if channel != '':
            logger.info("Collision!")
            time.sleep(random.uniform(0,5))
        else:
            logger.info("Send {}".format(times))
            send_encoded(encoded)
            times -= 1

            f = t.open('pipefile', 'r')
            channel = f.read().rstrip('\n')
            f.close()

            if channel == encoded:
                break

def byte_stuffing(text, flags):
    i = 0
    result = []
    for byte in list(text):
        if ord(byte) in flags:
            result.append(hex(flags[1]))
            encoded = hex(255-ord(byte))
            result.append(encoded)
        else:
            result.append(hex(ord(byte)))
    return result

def packet_forming(text, my_addr, dest_addr):
    size = len(text)
    crc = hex(count_crc(text))
    text.insert(0, hex(flags[0])) # beginning flag
    text.insert(1, hex(dest_addr)) # destination addr
    text.insert(2, hex(my_addr)) # source addr
    text.insert(3, hex(size)) # data size
    text.append(crc) # naive crc
    return text

def packet_output(arr):
    logger.info("\n======== PACKET STRUCTURE ========")
    logger.info("Beginning flag: {}".format(arr[0]))
    logger.info("Destination: {}".format(arr[1]))
    logger.info("Source flag: {}".format(arr[2]))
    logger.info("Data size: {}".format(arr[3]))
    logger.info("Data: {}".format(arr[4:len(arr)-1]))
    logger.info("Naive CRC: {}\n".format(arr[len(arr)-1]))

def count_crc(data):
    crc = 0
    for byte in data:
        crc += bin(int(byte, 16)).count('1')
    return crc

def byte_array_to_str(arr):
    result = ""
    for byte in arr:
        result += chr(int(byte, 16))
    return result

while(True):
    text = raw_input("")
    if text == "exit":
        f = t.open('pipefile', 'w')
        f.write("exit")
        f.close()
        os._exit(0)
    else:
        # print text
        stuffed = byte_stuffing(text, flags)
        # print stuffed
        packet_arr = packet_forming(stuffed, my_addr, dest_addr)
        # print packet_arr
        encoded = byte_array_to_str(packet_arr)
        # print encoded
        # packet_output(packet_arr)

        f = t.open('pipefile', 'r')
        channel = f.read().rstrip('\n')
        f.close()

        if channel != '':
            logger.info("Collision!")
            send_until(5)
        else:
            send_encoded(encoded)
            logger.info("Send {}".format(text))
