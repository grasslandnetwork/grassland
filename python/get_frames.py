import sys
import socket
import helper
import numpy as np
from PIL import Image
from hashlib import sha256
import time
import settings

from imutils.video import VideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS

import cv2
import numpy as np


host = '127.0.0.1'
port = settings.frames_port



def the_func(the_bytes):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    try:

        #beginning time
        begin=time.time()

        data = 0
        length = len(the_bytes)
        while data < length:
            data += client_socket.send(the_bytes) # 'sendall' instead of 'send' since we're not double checking number of bytes sent

            #if it's taking too long, stop
            if time.time()-begin > 3:
                # print("taking too long")
                break

        # print("time to write to socket", time.time()-begin)
            
    except:
        print("connection_problem")
    finally:
        client_socket.close()

    return client_socket



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




            
run_feed_loop = True
try:

    print("[INFO] starting video file stream...")
      
    main_fps = FPS().start()

    video_path = sys.argv[1]
    vs = FileVideoStream(video_path, queueSize=15).start()
    # loop over frames from the video stream
    while run_feed_loop:


        print(vs.more())
        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object

        frame = vs.read()

        # check to see if we have reached the end of the stream
        if frame is None:
            print("REACHED END OF CAMERA/VIDEO STREAM")
            break
        else:
            the_bytes = frame.tobytes('C') # https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.tobytes.html

            # join frame bytes to their sh256 checksum. Using ring hashing algorithm on client gives us 15 FPS. But that's before going to server. So maybe don't do this for local frames
            # bytes_payload = bytes(0).join( (the_bytes, sha256(the_bytes).digest()) )
            # client_socket = the_func(bytes_payload)

            client_socket = the_func(the_bytes)
            
            # print(len(the_bytes))
            # print(sha256(the_bytes).hexdigest())
            
            
        main_fps.update()


except:
    import traceback
    traceback.print_exc()

    
finally:                                                                                              
    
    
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
        print("Shutting down socket")
    except:
        pass

    try:
        client_socket.close()
    except:
        pass


    main_fps.stop()
    
    print("[INFO] elapsed time: {:.2f}".format(main_fps.elapsed()))
    print("[INFO] approx. Main FPS: {:.2f}".format(main_fps.fps()))


    sys.exit("Exiting")
