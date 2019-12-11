import sys
import json
#Here are the imports from the visualization module.
sys.path.append("node_python_files") 
import settings
# import helper


this_json = {
    "model_sha256_hash" : settings.MODEL_SHA256_HASH,
    "std_frame_dim" : {
        "width" : settings.std_frame_width,
        "height" : settings.std_frame_height
    },
    "frame_np_size": settings.frame_np_size,
    "ord_detection_output_meta_total_size" : settings.ord_detection_output_meta_total_size,
    "ord_detection_output_meta": {
        "frame_digest" : settings.ord_detection_output_meta['frame_digest']
    }
}


# json.dump(this_json, sys.stdout)

def int_to_two_bytes(integer_input):
    return integer_input.to_bytes(2, byteorder=settings.settings_byteorder)
    
def four_bytes_aligned_tuple(the_tuple):

    if len(the_tuple) == 0:
        return bytes(0).join(
            (
                int_to_two_bytes(0),
                int_to_two_bytes(0)
            )
        )

    elif len(the_tuple) == 1:
        return bytes(0).join(
            (
                int_to_two_bytes(the_tuple[0]),
                int_to_two_bytes(0)
            )
        )
    else:
        return bytes(0).join(
            (
                int_to_two_bytes(the_tuple[0]),
                int_to_two_bytes(the_tuple[1])
            )
        )
    

def get_detection_output_meta():
    the_bytes = b''
    for tensor in settings.output_tensor_names:
        the_bytes += bytes(0).join(
            (
                int_to_two_bytes(settings.ord_detection_output_meta[tensor]['total_bytes']),
                four_bytes_aligned_tuple(settings.ord_detection_output_meta[tensor]['strides']),
                four_bytes_aligned_tuple(settings.ord_detection_output_meta[tensor]['shape'])
            )
        )

        
    return the_bytes
                

    
std_frame_dim = bytes(0).join(
    (
        bytes.fromhex(settings.MODEL_SHA256_HASH),
        int_to_two_bytes(settings.std_frame_width),
        int_to_two_bytes(settings.std_frame_height),
        settings.frame_np_size.to_bytes(4, byteorder=settings.settings_byteorder),
        int_to_two_bytes(settings.ord_detection_output_meta_total_size),
        int_to_two_bytes(settings.ord_detection_output_meta['frame_digest']['total_bytes']),
        get_detection_output_meta(),
        int_to_two_bytes(settings.ord_detection_output_meta_total_size)
    )
) 



buffer_object = sys.stdout.buffer

# buffer_object.write(std_frame_dim)

buffer_object.write( bytes(0).join(( settings.detection_server.encode(), settings.port.encode() )) ) 

# buffer_object.write( bytes.fromhex(settings.MODEL_SHA256_HASH) )
# print(settings.ord_detection_output_meta['detection_scores']['strides'][1])
