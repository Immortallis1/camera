# File: eeh.py
# Description: Edge Enhancement
# Created: 2021/10/22 20:50
# Author: Qiu Jueqin (qiujueqin@gmail.com)


import numpy as np

from .basic_module import BasicModule, register_dependent_modules
from .helpers import generic_filter, gen_gaussian_kernel

import cv2
from .pipeline import ycbcr_to_rgb


@register_dependent_modules('csc')
class EEH(BasicModule):
    def __init__(self, cfg):
        super().__init__(cfg)

        kernel = gen_gaussian_kernel(kernel_size=5, sigma=1.2)
        self.gaussian = (1024 * kernel / kernel.max()).astype(np.int32)  # x1024

        t1, t2 = self.params.flat_threshold, self.params.edge_threshold
        threshold_delta = np.clip(t2 - t1, 1E-6, None)
        self.middle_slope = np.array(self.params.edge_gain * t2 / threshold_delta, dtype=np.int32)  # x256
        self.middle_intercept = -np.array(self.params.edge_gain * t1 * t2 / threshold_delta, dtype=np.int32)  # x256
        self.edge_gain = np.array(self.params.edge_gain, dtype=np.int32)  # x256

    def execute(self, data):
        y_image = data['y_image'].astype(np.int32)

        delta = y_image - generic_filter(y_image, self.gaussian)
        sign_map = np.sign(delta)
        abs_delta = np.abs(delta)

        middle_delta = np.right_shift(self.middle_slope * abs_delta + self.middle_intercept, 8)
        edge_delta = np.right_shift(self.edge_gain * abs_delta, 8)
        enhanced_delta = (
                (abs_delta > self.params.flat_threshold) * (abs_delta <= self.params.edge_threshold) * middle_delta +
                (abs_delta > self.params.edge_threshold) * edge_delta
        )

        enhanced_delta = sign_map * np.clip(enhanced_delta, 0, self.params.delta_threshold)
        eeh_y_image = np.clip(y_image + enhanced_delta, 0, self.cfg.saturation_values.sdr)

        data['y_image'] = eeh_y_image.astype(np.uint8)
        data['edge_map'] = delta

        ycbcr_image = np.dstack([data['y_image'][..., None], data['cbcr_image']])
        out = ycbcr_to_rgb(ycbcr_image)
        cv2.imwrite('./Image/after_eeh.jpg',cv2.cvtColor(out,cv2.COLOR_RGB2BGR))
