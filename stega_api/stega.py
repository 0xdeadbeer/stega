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

def frombits(bits):
    chars = []
    for b in range(len(bits) / 8):
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

def stega_function(data, location): 
    data_bit_array = tobits(data) 
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

    if ((y_range_width * x_range_width) <= len(data_bit_array)):
        return {
            "Type": "Error",
            "Message": "Data cannot fit into the image"
        }

    try: 
            
        for y_index in range(y_pos, y_end): 
            for x_index in range(x_pos, x_end):
                index = ((y_index - y_pos) * y_range_width) + (x_index - x_pos)

                try: 
                    the_bit = data_bit_array[index] 
                    r,g,b = image_data[y_index][x_index]

                    if (index % 2 == 0): 
                        r = set_bit(r, 0, the_bit)
                    elif (index % 7 == 0):
                        g = set_bit(g, 1, the_bit)
                    else:
                        b = set_bit(b, 0, the_bit) 
                    new_rgb = [r, g, b]

                    image_data[y_index][x_index] = new_rgb

                except Exception as e: 

                    # alright we're done here 
                    raise Found 

    except Found: 
        new_location = os.path.splitext(location)[0] + ".hid.png"

        cv2.imwrite(new_location, image_data)
        return {
            "Type": "Success", 
            "Message": new_location
        }
    
    except Exception: 
        return {
            "Type": "Error",
            "Message": "Server error, please report this problem to Osamu"
        }
