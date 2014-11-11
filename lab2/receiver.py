import pipes
import os
import sys

flags = [0x65, 0xFF]

if len(sys.argv) > 1:
    my_addr = sys.argv[1]
else:
    my_addr = 13

def decode_packet(str, my_addr):
    result = []
    for byte in str:
        result.append(hex(ord(byte)))
    dst = int(result[1], 16)
    source = int(result[2], 16)
    size = int(result[3], 16)
    data = result[4:len(result)-1]
    crc = int(result[len(result)-1], 16)
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
            t = pipes.Template()
            f1 = t.open('pipefile', 'w')
            f1.write('')
            f1.close
            os._exit(0)
        correct_addr, correct_crc, str_new = decode_packet(str, my_addr)
        if correct_addr and correct_crc:
            print str_new
    str_last = str
