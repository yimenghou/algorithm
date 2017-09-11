import cv2
import numpy as np

winSize = (20, 20)
blockSize = (8, 8)
blockStride = (4, 4)
cellSize = (4, 4)
nbins = 9

img = np.zeros(winSize, dtype=np.uint8)

hogger = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins)

img_o = hogger.compute(img)

print img_o.shape