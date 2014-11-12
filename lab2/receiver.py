import pipes
import os
import sys
import logging

logging.basicConfig(filename='info.log',level=logging.INFO)
logger = logging.getLogger("Receiver")

flags = [0x65, 0xFF]
t = pipes.Template()

if len(sys.argv) > 1:
    my_addr = sys.argv[1]
else:
    my_addr = 13

def decode_packet(str, my_addr):
    result = []
    for byte in str:
        result.append(hex(ord(byte)))
    if result[0] != hex(flags[0]):
        return False, False, ''
    if len(result) > 0 and len(result) < 6:
        return False, False, ''
    dst = int(result[1], 16)
    if dst != my_addr:
        return False, False, ''
    source = int(result[2], 16)
    size = int(result[3], 16)
    data = result[4:size+4]
    crc = int(result[size+4], 16)
    new_crc = count_crc(data)
    data_unstuffed = byte_unstuffing(data)
    str_new = byte_array_to_str(data_unstuffed)
    return dst == my_addr, crc == new_crc, str_new

def count_crc(data):
    crc = 0
    for byte in data:
        crc += bin(int(byte, 16)).count('1')
    return crc

def byte_unstuffing(data):
    result = []
    i = 0
    while i < len(data):
        if data[i] == hex(flags[1]):
            result.append(hex(255 - int(data[i+1], 16)))
            i += 1
        else:
            result.append(data[i])
        i += 1
    return result

def byte_array_to_str(data):
    result = ""
    for byte in data:
        result += chr(int(byte, 16))
    return result

str_last = ''
while (True):
    str = open('pipefile', 'r').read().rstrip('\n')
    if str_last != str and str != '':
        if str == 'exit':
            f1 = t.open('pipefile', 'w')
            f1.write('')
            f1.close
            os._exit(0)
        correct_addr, correct_crc, str_new = decode_packet(str, my_addr)
        if correct_addr and correct_crc:
            print str_new
            logger.info("Received {}".format(str_new))
        #else:
            #logger.info("Received incorrect message")
    str_last = str
