# File: blc.py
# Description: Black Level Compensation
# Created: 2021/10/22 20:50
# Author: Qiu Jueqin (qiujueqin@gmail.com)


import numpy as np

from .basic_module import BasicModule
from .helpers import split_bayer, reconstruct_bayer
import cv2


class BLC(BasicModule):
    def __init__(self, cfg):
        super().__init__(cfg)

        self.alpha = np.array(self.params.alpha, dtype=np.int32)  # x1024
        self.beta = np.array(self.params.beta, dtype=np.int32)  # x1024

    def execute(self, data):
        bayer = data['bayer'].astype(np.int32)

        r, gr, gb, b = split_bayer(bayer, self.cfg.hardware.bayer_pattern)

        r_0, gr_0, gb_0, b_0 = split_bayer(data['b'], self.cfg.hardware.bayer_pattern)
        r = np.clip(r - r_0, 0, None) # self.params.bl_r
        b = np.clip(b - b_0, 0, None) # self.params.bl_b
        gr -= (gr_0 - np.right_shift(r * self.alpha, 10)) # self.params.bl_gr
        gb -= (gb_0 - np.right_shift(b * self.beta, 10)) # self.params.bl_gb
        blc_bayer = reconstruct_bayer(
            (r, gr, gb, b), self.cfg.hardware.bayer_pattern
        )

        data['bayer'] = np.clip(blc_bayer, 0, None).astype(np.uint16)

        data['blc'] = data['bayer']


