# File: fcs.py
# Description: False Color Suppression
# Created: 2021/10/22 20:50
# Author: Qiu Jueqin (qiujueqin@gmail.com)


import numpy as np

from .basic_module import BasicModule, register_dependent_modules

import cv2
from .pipeline import ycbcr_to_rgb


@register_dependent_modules(('csc', 'eeh'))
class FCS(BasicModule):
    def __init__(self, cfg):
        super().__init__(cfg)

        threshold_delta = np.clip(self.params.delta_max - self.params.delta_min, 1E-6, None)
        self.slope = -np.array(65536 / threshold_delta, dtype=np.int32)  # x65536

    def execute(self, data):
        cbcr_image = data['cbcr_image'].astype(np.int32)
        edge_map = data['edge_map']

        gain_map = self.slope * (np.abs(edge_map) - self.params.delta_max)
        gain_map = np.clip(gain_map, 0, 65536)
        fcs_cbcr_image = np.right_shift(gain_map[..., None] * (cbcr_image - 128), 16) + 128
        fcs_cbcr_image = np.clip(fcs_cbcr_image, 0, self.cfg.saturation_values.sdr)

        data['cbcr_image'] = fcs_cbcr_image.astype(np.uint8)

        ycbcr_image = np.dstack([data['y_image'][..., None], data['cbcr_image']])
        out = ycbcr_to_rgb(ycbcr_image)
        cv2.imwrite('./Image/after_fcs.jpg',cv2.cvtColor(out,cv2.COLOR_RGB2BGR))
