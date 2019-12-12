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


from collections import OrderedDict

# Security check for Grassland model
MODEL_SHA256_HASH = 'fa2cef2ed0543933f132539bd037fa9b66a73d9a33c660cedf68961a880a068f'

# Video Frame Dimensions
std_frame_width = 1920
std_frame_height = 1080


frame_np_size =  std_frame_width * std_frame_height * 3 # '* 3' because it's a raster


detection_np_dtype = '<f4'  # little-endian float32 is the default output of the Eon 0 detection model

# Make tuple (immutable) of output tensor names
output_tensor_names = ('detection_boxes','detection_scores','detection_classes','num_detections')


# STANDARDIZED SIZES (IN BYTES) FOR INTERNAL AND EXTERNAL DETECTION VALUES 
ord_detection_output_meta = OrderedDict() # 'settings.ord_detection_output_meta' MUST be an Ordered Dictionary
ord_detection_output_meta['frame_digest'] = {'total_bytes': 32}

# "detections" outputs are numpy arrays and require extra information to rebuild them. They are all detection_np_dtype
ord_detection_output_meta['detection_boxes'] = {'total_bytes': 1600, 'strides': (16, 4), 'shape': (100, 4)}
ord_detection_output_meta['detection_scores'] = {'total_bytes': 400, 'strides': (4,), 'shape': (100,)}
ord_detection_output_meta['detection_classes'] = {'total_bytes': 400, 'strides': (4,), 'shape': (100,)}
ord_detection_output_meta['num_detections'] = {'total_bytes': 4, 'strides': (), 'shape': ()} # num_detections has 0 dimensions

ord_detection_output_meta['detection_digest'] = {'total_bytes': 32}
ord_detection_output_meta['hidden_activations_digest'] = {'total_bytes': 32}
ord_detection_output_meta['reserved_digest'] = {'total_bytes': 32}

# Total Size in bytes of returned data,
# ...boxes, scores, classes, num and the four digests (frame, detection, hidden, reserved) should be 2532 bytes
ord_detection_output_meta_total_size = 0
for key, val in ord_detection_output_meta.items():
    ord_detection_output_meta_total_size += val['total_bytes']



EON_0_WANTED_TENSORS = [
    'ExpandDims_4', 
    'SecondStageFeatureExtractor/InceptionV2/Mixed_5b/Branch_3/AvgPool_0a_3x3/AvgPool',
    'SecondStagePostprocessor/BatchMultiClassNonMaxSuppression/map/while/PadOrClipBoxList/cond_3/Merge',
    # 'BatchMultiClassNonMaxSuppression/map/TensorArray',
    'SecondStageFeatureExtractor/InceptionV2/Mixed_5c/Branch_1/Conv2d_0b_3x3/Conv2D',
    'SecondStageFeatureExtractor/InceptionV2/Mixed_5b/Branch_2/Conv2d_0c_3x3/Relu',
    'SecondStageFeatureExtractor/InceptionV2/Mixed_5c/Branch_3/MaxPool_0a_3x3/MaxPool',
    'SecondStageFeatureExtractor/InceptionV2/Mixed_5b/Branch_1/Conv2d_0b_3x3/Conv2D',
    'SecondStageFeatureExtractor/InceptionV2/Mixed_5c/Branch_3/Conv2d_0b_1x1/BatchNorm/FusedBatchNorm',
    'map_1/while/TensorArrayReadV3',
    'map_1/TensorArrayStack/TensorArrayGatherV3',
    'detection_boxes',
    'detection_scores',
    'detection_classes',
    #'detection_masks',
    'num_detections',
]


STREAM_TYPE = 'ndarray_bytes'
