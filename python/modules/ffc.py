import numpy as np

from .basic_module import BasicModule
import cv2

class FFC(BasicModule):
    def execute(self, data):
        bayer = data['bayer'].astype(np.int32)
        
        w = data['w']
        b = data['b']
        bayer = (bayer - b) / (w - b) * np.mean(w - b)

        data['bayer'] = bayer.astype(np.uint16)

        cv2.imwrite('./Image/after_ffc.jpg',data['bayer'])

