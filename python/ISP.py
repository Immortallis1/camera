import cv2
import numpy as np
from modules.pipeline import Pipeline
from yacs import Config


class ISP():
    def __init__(self,dir):
        self.dir = dir
        self.img = cv2.imread(f"{self.dir}/raw.jpg",cv2.IMREAD_UNCHANGED)



    def save(self):
        LT = cv2.cvtColor(self.LT['output'], cv2.COLOR_RGB2BGR)
        cv2.imwrite(f"{self.dir}/img_LT.jpg", LT)
        cv2.imwrite(f"{self.dir}/img_LB.jpg", self.LB)
        cv2.imwrite(f"{self.dir}/img_RT.jpg", self.RT)
        cv2.imwrite(f"{self.dir}/img_RB.jpg", self.RB)

    def QUAD_IMG(self):
        self.LT, self.LB, self.RT, self.RB = (np.zeros((self.img.shape[0]//4,self.img.shape[1])).astype(np.uint8),
                                              np.zeros((self.img.shape[0]//4,self.img.shape[1])).astype(np.uint8),
                                              np.zeros((self.img.shape[0]//4,self.img.shape[1])).astype(np.uint8),
                                              np.zeros((self.img.shape[0]//4,self.img.shape[1])).astype(np.uint8))
        for i in range(self.img.shape[0]//4):
            self.LT[i,:] = self.img[4*i,:,0]
            self.LB[i,:] = self.img[4*i+1,:,0]
            self.RT[i,:] = self.img[4*i+2,:,0]
            self.RB[i,:] = self.img[4*i+3,:,0]

        self.quad_img = {'LT': self.LT,
                         'LB': self.LB,
                         'RT': self.RT,
                         'RB': self.RB}


    def processing(self, tag):
        cfg = Config('./python/config/test.yaml')
        pipeline = Pipeline(cfg, tag, self.dir)
        self.LT, _ = pipeline.execute(self.quad_img[tag])

     









