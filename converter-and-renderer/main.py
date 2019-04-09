
import converter
import banana
import cv2
import numpy as np



imgPathIn = 'output/annotated_0006.png'
backPathIn = 'plantation.jpg'
imgPathOut = 'output/test.jpg'
converter.main("data/ModelNet10/monitor/test/monitor_0466.off","data/test.obj","obj",None,None)
banana.peel(10,0.3) # (Number of viewpoints, Distance from model)
banana.changeBackground(imgPathIn,backPathIn,imgPathOut)
# banana.look() # Visualize model



