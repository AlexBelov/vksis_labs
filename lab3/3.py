import math
import numpy as np
import random
import sys
import logging

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

setup_logger('log1', r'info.log')
setup_logger('log2', r'out.log')
log1 = logging.getLogger('log1')
log2 = logging.getLogger('log2')

if len(sys.argv) == 2:
    insert_error = True
else:
    insert_error = False

def bin_to_vector(num, height):
    result = []
    binary = list(bin(num)[2:].zfill(height))
    for b in binary:
        result.append([int(b)])
    return result[::-1]

while(True):
    string = raw_input('').rstrip('\n')

    binary_str = []
    for char in string:
        binary_str += list(bin(ord(char))[2:].zfill(8))

    # print binary_str

    length = len(binary_str)
    width = int(math.ceil(length + math.log(length, 2))) + 1
    height = int(math.ceil(math.log(width, 2))+1)

    # print len(binary_str)
    # print width
    # print height

    width += 1
    hamming_matrix = np.zeros((height, width))

    i = 0
    j = 0
    for i in range(width):
        if i == 0 or math.log(i,2).is_integer():
            hamming_matrix[0][i] = 0
        else:
            hamming_matrix[0][i] = binary_str[j]
            if j < len(binary_str)-1:
                j += 1
        i += 1

    i = 0
    for i in range(width):
        hamming_matrix[1:,[i]] = bin_to_vector(i, height-1)

    # print hamming_matrix

    control_bits = []
    for j in range(1, height):
        sum = 0
        for i in range(1, width):
            if hamming_matrix[j][i] == 1:
                sum += hamming_matrix[0][i]
        if sum % 2 == 0:
            control_bits.append(0)
        else:
            control_bits.append(1)

    j = 0
    for i in range(1, width):
        if math.log(i,2).is_integer():
            hamming_matrix[0][i] = control_bits[j]
            j += 1

    hamming_encoded = hamming_matrix[[0],:]

    #print ''.join(map(str, map(int, hamming_encoded[0][1:])))

    # ==== INSERT ONE ERROR

    if insert_error:
        error_index = random.randint(1, len(hamming_encoded[0])-1)

        if hamming_encoded[0][error_index] == 0:
            hamming_encoded[0][error_index] = 1
        else:
            hamming_encoded[0][error_index] = 0

    # ==== INSERT ONE ERROR

    log1.info(''.join(map(str, map(int, hamming_encoded[0][1:]))))

    hamming_matrix = np.zeros((height, width))
    hamming_matrix[0] = hamming_encoded

    i = 0
    for i in range(width):
        hamming_matrix[1:,[i]] = bin_to_vector(i, height-1)

    control_bits_old = []
    for i in range(1, width):
        if math.log(i,2).is_integer():
            control_bits_old.append(int(hamming_matrix[0][i]))

    control_bits = []
    for j in range(1, height):
        sum = 0
        for i in range(1, width):
            if hamming_matrix[j][i] == 1:
                sum += hamming_matrix[0][i]
        if sum % 2 == 0:
            control_bits.append(0)
        else:
            control_bits.append(1)

    #print hamming_matrix
    #print control_bits_old
    control_bits = control_bits[::-1]
    #print control_bits

    error_position = int(''.join(map(str, control_bits)), 2)
    #print error_position

    if hamming_encoded[0][error_position] == 0:
        hamming_encoded[0][error_position] = 1
    else:
        hamming_encoded[0][error_position] = 0

    #print ''.join(map(str, map(int, hamming_encoded[0][1:])))

    arr_decoded = []
    for i in range(1, len(hamming_encoded[0])):
        if not math.log(i,2).is_integer():
            arr_decoded.append(int(hamming_encoded[0][i]))

    #print arr_decoded

    str_decoded = ''
    i = 0
    while i<len(arr_decoded):
        str_decoded += chr(int(''.join(map(str, arr_decoded[i:i+8])), 2))
        i += 8

    log2.info(str_decoded)
