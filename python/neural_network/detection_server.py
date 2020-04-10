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
import os
from PIL import Image
from urllib import request
import socket
from hashlib import sha256
#import io
import time

import settings
import helper
from detection_inference import DetectionModel

import sys

#Here are the imports from the visualization module.
sys.path.append("tensorflow_repos/models/research/") 
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import ops as utils_ops


PATH_TO_LABELS = os.path.join('tensorflow_repos/models/research/object_detection/data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90

#Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)



# Grassland model variables
MODEL_NAME = 'eon_0'
MODEL_FILE = MODEL_NAME + '.pb'
MODEL_PATH = 'models/' + MODEL_FILE


#stream_type = 'image'
stream_type = 'ndarray_bytes'


def verify_model_is_downloaded():
    # Check if current eon's model has been downloaded
    exists = os.path.isfile(MODEL_PATH)
    if not exists:
        #Download Model
        print("Grassland eon models not found. Downloading...")
        DOWNLOAD_BASE = 'https://downloads.grassland.network/models/'
        opener = request.URLopener()
        opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_PATH)


# host = 'localhost'
# host = '127.0.0.1'
host = '0.0.0.0'
#port = 8000
port = 8888
address = (host,port)

# buffer_size = 4096
buffer_size = 6220800


def create_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # https://stackoverflow.com/a/6380198/8941739
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

    server_socket.bind(address)
    server_socket.listen(5)

    return server_socket


    
def connect_to_socket(server_socket):
    print("Starting connection")
    print("Listening for new client . . .")

    while True:
        conn, address = server_socket.accept() # Blocks until it receives connect from other end

        # def check_verack()
        magic_bytes = conn.recv(4)
        if magic_bytes == bytes.fromhex('F9BEB5D9'):
            print("MAGIC BYTES RECEIVED")
            break

        
        # else it's not a connection we want. drop it
        conn.close()
        time.sleep(3)

        
    makefile_conn = conn.makefile('rb')
    print("Connected to client at ", address)
    
    return conn, makefile_conn
    
    
def disconnect_from_socket(conn, makefile_conn):
    print("Closing connection . . .")
    makefile_conn.close()
    conn.close()
    time.sleep(3)
    


def main():
    
    verify_model_is_downloaded()

    # Construct instance of DetectionModel
    detection_model = DetectionModel(MODEL_PATH)

    try:
        RECONNECT = False 
        server_socket = create_socket()

        print("Detection Server started with Stream Type =", stream_type)

        conn, makefile_conn = connect_to_socket(server_socket)

        while True:
            try:

                if RECONNECT:
                    print("disconnect from client")
                    disconnect_from_socket(conn, makefile_conn)

                    print("wait for connection to client")
                    conn, makefile_conn = connect_to_socket(server_socket)

                    RECONNECT = False

                # Construct a stream to hold the image data and read the image data from the connection
                frame_np_bytes = makefile_conn.read(buffer_size)

                #frame_np_bytes = conn.recv(buffer_size)
#
                if len(frame_np_bytes) > 0:

                    if frame_np_bytes.startswith(bytes.fromhex('F9BEB5D9')):
                        RECONNECT = True
                        continue

                    # print("frame_np_bytes", frame_np_bytes[0:8])

                    if settings.frame_np_size != len(frame_np_bytes):
                        print("Transmitted object's length is", len(frame_np_bytes), "bytes. Expected length of",settings.frame_np_size, "bytes")
                        continue

                    # the_stream = io.BytesIO()
                    # the_stream.write(frame_np_bytes)

                    # the_stream.flush()

                    # # Rewind the stream
                    # the_stream.seek(0)

                    start = time.time()

                    #image_np = helper.load_binary_file_into_standard_image_np_array(the_stream)

                    image_np = helper.convert_buffer_object_into_standard_image_np_array(memoryview(frame_np_bytes))

                    
                    # Run inference
                    output_dict = detection_model.runInference(image_np)
                    # print("output_dict ", output_dict)


                    # print("num_detections tobytes", output_dict['num_detections'].tobytes())

                    # MAKE FRAME (INPUT) DIGEST
                    output_dict["frame_digest"] = sha256(image_np.tobytes()).digest()

                    # print("frame_digest", sha256(image_np.tobytes()).hexdigest())

                    # MAKE DETECTIONS (OUTPUT) DIGEST
                    # ... by making rolling hash of just output tensors using...
                    # ... https://docs.python.org/3.6/library/hashlib.html#hashlib.hash.update
                    m = sha256() 
                    for tensor_name in settings.output_tensor_names:
                        # ensuring all tensors (ndarray) data has the correct endianness and dtype
                        m.update( output_dict[tensor_name].astype(settings.detection_np_dtype).tobytes() )

                    output_dict["detection_digest"] = m.digest()


                    # MAKE HIDDEN ACTIVATIONS DIGEST AND RESERVED DIGEST                
                    # Create copy of settings.EON_0_WANTED_TENSORS list...
                    hidden_tensors = settings.EON_0_WANTED_TENSORS.copy()
                    # ...but only keep hidden layers
                    for tensor_name in settings.output_tensor_names: 
                        hidden_tensors.remove(tensor_name)

                    hidden_activations_digest = bytes(0)
                    reserved_digest = bytes(0)
                    for tensor_name in hidden_tensors:

                        if type(output_dict[tensor_name]) == np.ndarray:
                            
                            if tensor_name == hidden_tensors[0]: # First loop
                                hidden_activations_digest = frame_np_bytes # Has [3*width*height] bytes. High pseudo randomness
                            
                            # Concatenate old hidden_activations_digest and current hidden tensor array bytes object ensuring all tensors (ndarray) data has the correct endianness and dtype
                            merged = bytes(0).join( ( hidden_activations_digest, output_dict[tensor_name].astype(settings.detection_np_dtype).tobytes() ) )

                            # Set the digest of the numpy array as the new hidden_activations_digest
                            hidden_activations_digest = sha256(merged).digest()

                            if tensor_name == hidden_tensors[-2]: # penultimate hidden layer
                                reserved_digest = hidden_activations_digest


                    output_dict["hidden_activations_digest"] = hidden_activations_digest
                    output_dict["reserved_digest"] = reserved_digest


                    # print("ord_detection_output_meta_total_size", settings.ord_detection_output_meta_total_size)
                    # print("ABOUT TO SEND ALL DETECTIONS")

                    # Place each of the detection output bytes objects in a list
                    bytes_list = []
                    for key in settings.ord_detection_output_meta.keys(): # 'settings.ord_detection_output_meta' MUST be an Ordered Dictionary
                        if "digest" in key:
                            bytes_list.append( output_dict[key] )
                        else:
                            bytes_list.append( output_dict[key].tobytes() )

                        # print("-------------------------------------------------------------------------------------------------------------------------")
                        # print("key => ", key) 
                        # print("output value => ", output_dict[key])
                        # print("-------------------------------------------------------------------------------------------------------------------------")

 
                    # print(" bytes_list --------------------------------------------------------------------------------------------------------------------")
                    # print(bytes_list)
                    # print(" end of bytes_list --------------------------------------------------------------------------------------------------------------")
                    # print("----------------------------------------------------------------------------------------------------------------------------------")

                    # Take each of the detection output values in bytes_list and concatenate them into a single bytes like object
                    detections_and_digests_encoded = bytes(0).join(bytes_list)

                    # print("size of detections_and_digests_encoded is", len(detections_and_digests_encoded))


                    #print("second output_dict ...................................................................")
                    #print(output_dict)
                    #print("above was second output_dict ............................................................................................")

                    # print("detections_and_digests_encoded ", detections_and_digests_encoded.hex())

                    print("sha256 hash of detections_and_digests_encoded ", sha256(detections_and_digests_encoded).hexdigest())

                    print("length of detections_and_digests_encoded", len(detections_and_digests_encoded))

                    # Send them to client
                    conn.sendall(detections_and_digests_encoded)
                    # conn.send(detections_and_digests_encoded)                 

                    # print("disconnecting from python client")
                    # disconnect_from_socket(conn, makefile_conn)
                    #print("wait for connection to rust client")
                    #conn, makefile_conn = connect_to_socket(server_socket)
                    #print("send data to rust client")
                    #conn.sendall(detections_and_digests_encoded)
                    #print("disconnect from client")
                    #disconnect_from_socket(conn, makefile_conn)



            except KeyboardInterrupt:
                print("Waiting for second interrupt to exit program")
                time.sleep(1)
                RECONNECT = True
                #raise

            except:
                import traceback
                traceback.print_exc()

                print("...SOMETHING HAPPENED...")

                data = ""

                disconnect_from_socket(conn, makefile_conn)
                conn, makefile_conn = connect_to_socket(server_socket)

                RECONNECT = False


        
    except:
        import traceback
        traceback.print_exc()

    finally:
        detection_model.close()
        try:
            disconnect_from_socket(conn, makefile_conn)
        except:
            pass

        print("Shutting down socket")
        server_socket.shutdown(socket.SHUT_RDWR)
        
        print("Closing socket")
        server_socket.close()
        sys.exit("Received disconnect message.  Shutting down.")


    

        
if __name__ == '__main__':
    main()



            





