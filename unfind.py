#!/usr/bin/python3 
import os 
import sys 
import cv2
from cv2 import imshow 
import numpy as np 

class Found(Exception): pass

def read_image(location): 
    img = cv2.imread(location, 1) 
    return img

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def binary_to_unicode(data) :
    output_string = ""
    for binary_value in data: 
        integer = int(binary_value, 2)
        char = chr(integer) 
        output_string += str(char) 
    return output_string

def frombits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def set_bit(v, index, x):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask         # If x was True, set the bit indicated by the mask.
    return v            # Return the result, we're done.

def get_bit(v, index):
    return (v >> index) & 1

def split_binary(data, n): 
    return [data[i:i+n] for i in range(0, len(data), n)]

def main(): 
    the_output = []
    location = input("Enter image location: ")
    image_data = read_image(location) 

    cx = 4 
    cy = 5 

    x, y, rgb = image_data.shape

    x_pos = int(x / cx)
    y_pos = int(y / cy)

    x_end = int(x - x_pos) 
    y_end = int(y - y_pos)

    y_range_width = x_end - x_pos
    x_range_width = y_end - y_pos

    for y_index in range(y_pos, y_end): 
        for x_index in range(x_pos, x_end):
            index = ((y_index - y_pos) * y_range_width) + (x_index - x_pos)

            # [DEBUG]
            # print ("Pixel: y -> " + str(y_index) + ", x -> " + str(x_index) + ", index -> " + str(index)) 

            r,g,b = image_data[y_index][x_index]
            the_sus_bit = 0
            if (index % 2 == 0): 
                the_sus_bit = get_bit(r, 0)
            elif (index % 7 == 0):
                the_sus_bit = get_bit(g, 1)
            else:
                the_sus_bit = get_bit(b, 0) 

            the_output.append(the_sus_bit)

    output_string = ''.join(str(x) for x in the_output)
    output_string = split_binary(output_string, 8)
    output_string = binary_to_unicode(output_string)
    print ("Inspect the output from the image, it may contain the message :)")
    print ("----------------------------------------")
    print (output_string.split())
    print ("----------------------------------------")

if __name__ == "__main__":
    main() 