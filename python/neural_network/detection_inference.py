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
import sys
import tensorflow as tf
import time
import struct
import json
from hashlib import sha256
import settings


# https://stackoverflow.com/questions/11887762/how-do-i-compare-version-numbers-in-python
from distutils.version import LooseVersion, StrictVersion
if LooseVersion(tf.__version__) < LooseVersion("1.4.0"):
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')



class DetectionModel:
    def __init__(self, MODEL_PATH):
        # Parts of this "__init__" "method adapted from https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb 
        self.MODEL_PATH = MODEL_PATH

        # Security check to make sure your Grassland model is the right one
        if self.model_checksum(self.MODEL_PATH) != settings.MODEL_SHA256_HASH:
            raise ValueError('GRASSLAND MODEL DOES NOT PASS CHECKSUM. YOU COULD BE BEING ATTACKED!')
        else:
            print('MODEL CHECKSUM SUCCESSFUL')

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.MODEL_PATH, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')


        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)
        # self.sess = tf.Session(graph=self.detection_graph, config=tf.ConfigProto(log_device_placement=True)) # Uncommment if you want to print to console if running on GPU or CPU 


        # GET HANDLE TO INPUT AND OUTPUT TENSORS FOR detection_graph
        # >>>
        
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        
        ops = self.detection_graph.get_operations()
        all_tensor_names = {output.name for op in ops for output in op.outputs}
        self.tensor_dict = {}
        for key in settings.EON_0_WANTED_TENSORS:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
                self.tensor_dict[key] = self.detection_graph.get_tensor_by_name(tensor_name)

        # <<<

                
    def runInference(self, image_np):

        try:
            start = time.time()
            
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)

            output_dict = self.sess.run(self.tensor_dict, feed_dict={self.image_tensor: image_np_expanded})
            print("Inference time took " + str(time.time() - start))

            # all outputs are little endian, float32 numpy arrays
            
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0].astype(settings.detection_np_dtype)
            output_dict['detection_scores'] = output_dict['detection_scores'][0].astype(settings.detection_np_dtype)
            output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(settings.detection_np_dtype)
            output_dict['num_detections'] = output_dict['num_detections'][0].astype(settings.detection_np_dtype)


            return output_dict
            
        except:
            import traceback
            traceback.print_exc()

            self.close()



    @staticmethod
    def model_checksum(MODEL_PATH): # https://stackoverflow.com/a/3431838/8941739
        m = sha256()
        with open(MODEL_PATH, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                m.update(block)
            return m.hexdigest()



    def close(self):
        self.sess.close()


