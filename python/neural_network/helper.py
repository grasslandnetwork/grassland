# Copyright (C) 2018-2019 David Thompson
#
# This file is part of Grassland
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of Grassland, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.


import numpy as np
import settings
from hashlib import sha256

class MyException(Exception):
    pass

#Numpy Helper Code
def convert_array_like_into_standard_detection_np_array(new_array):
    
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.asarray.html
    return np.asarray(new_array, dtype=settings.detection_np_dtype, order='C').astype('<f4') 


def convert_array_like_into_standard_image_np_array(new_array):
    # 'uint8': 8 bit number since images are 0-255. No endianness incompatibility problems between machines and to prevent cheating by using the same frame but getting different hashes by changing number precision
    
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.asarray.html
    return np.asarray(new_array, dtype='uint8', order='C') 


def load_image_into_standard_image_np_array(image): # Argument is a PIL image
    (im_width, im_height) = image.size # Get dimensions of 'image' argument
    if im_width != settings.std_frame_width or im_height != settings.std_frame_height:
        raise MyException("!!! Image dimensions are incorrect. Standard dimensions are width:"+str(settings.std_frame_width)+", height:"+str(settings.std_frame_height)+". Received image with dimensions width:"+str(im_height)+", height:"+str(im_height)+" !!!!")
      
    new_array = np.array(image.getdata()).reshape((im_height, im_width, 3))

    return convert_array_like_into_standard_image_np_array(new_array)


def convert_buffer_object_into_standard_image_np_array(buffer_object):

    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.frombuffer.html
    new_array = np.frombuffer(buffer_object, dtype='uint8', count=-1, offset=0).reshape((settings.std_frame_height, settings.std_frame_width, 3)) 
    
    return convert_array_like_into_standard_image_np_array(new_array)


def load_binary_file_into_standard_image_np_array(the_stream):
    the_stream.seek(0) # Seek to beginning just in case

    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.frombuffer.html
    new_array = np.frombuffer(the_stream.getbuffer(), dtype='uint8', count=-1, offset=0).reshape((settings.std_frame_height, settings.std_frame_width, 3)) 
    
    return convert_array_like_into_standard_image_np_array(new_array)


def load_bytes_object_into_standard_detection_np_array(bytes_object, shape=None):
    
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.frombuffer.html
    new_array = np.frombuffer(bytes_object, dtype=settings.detection_np_dtype, count=-1, offset=0)
    
    if shape != None: # Don't use 'if shape:' because if 'shape' is '()', it'll execute the 'else' statement cause '()' is 'Falsy'...
        # ... and your array will have 1 dimension even if you want it to have 0
        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.reshape.html#numpy.ndarray.reshape
        return new_array.reshape(shape, order='C')
    else: # Just interpret the array as is
        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.asarray.html
        return np.asarray(new_array, order='C') 

    
# DOUBLE DIGESTS
# page counts -> https://en.wikipedia.org/w/index.php?title=Jughead%27s_Double_Digest&oldid=816697808#Publication_history
def old_jughead(bytes_object): # Outputs 256 bit digest hash. SHA256( SHA256() )
    return sha256( sha256(bytes_object).digest() ).digest()

def new_jughead(bytes_object): # Outputs 160 bit digest hash. Ripemd160( SHA256() )
    h_ripe = hashlib.new('ripemd160p')
    h_ripe.update( sha256(bytes_object).digest() )
    return h_ripe.digest()



