import math
import numpy as np

def bin_to_vector(num, height):
    result = []
    binary = list(bin(num)[2:].zfill(height))
    for b in binary:
        result.append([int(b)])
    return result[::-1]

str = 'h'

binary_str = []
for char in str:
    binary_str += list(bin(ord(char))[2:].zfill(8))

length = len(binary_str)
width = int(math.ceil(length + math.log(length, 2)))
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
    #     print '!'
    # print hamming_matrix[0][i]

hamming_encoded = hamming_matrix[[0],1:]
print control_bits
print hamming_encoded
