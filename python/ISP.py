import cv2
import numpy as np
from modules.pipeline import Pipeline
from yacs import Config

class ISP():
    def __init__(self,dir):
        self.dir = dir
        self.img = cv2.imread(f"{self.dir}.jpg",cv2.IMREAD_UNCHANGED)
        self.QUAD_IMG(self.img)
        self.processing(self.LT, 'LT')



    def save(self):
        LT = cv2.cvtColor(self.LT['output'], cv2.COLOR_RGB2BGR)
        cv2.imwrite(f"{self.dir}_LT.jpg", LT)
        cv2.imwrite(f"{self.dir}_LB.jpg", self.LB)
        cv2.imwrite(f"{self.dir}_RT.jpg", self.RT)
        cv2.imwrite(f"{self.dir}_RB.jpg", self.RB)

    def QUAD_IMG(self,img):
        self.LT, self.LB, self.RT, self.RB = (np.zeros((img.shape[0]//4,img.shape[1])).astype(np.uint8),
                                              np.zeros((img.shape[0]//4,img.shape[1])).astype(np.uint8),
                                              np.zeros((img.shape[0]//4,img.shape[1])).astype(np.uint8),
                                              np.zeros((img.shape[0]//4,img.shape[1])).astype(np.uint8))
        for i in range(img.shape[0]//4):
            self.LT[i,:] = img[4*i,:,0]
            self.LB[i,:] = img[4*i+1,:,0]
            self.RT[i,:] = img[4*i+2,:,0]
            self.RB[i,:] = img[4*i+3,:,0]

    def processing(self, img, tag):
        cfg = Config('./python/samples/config/test.yaml')
        pipeline = Pipeline(cfg, tag)
        self.LT, _ = pipeline.execute(img)









