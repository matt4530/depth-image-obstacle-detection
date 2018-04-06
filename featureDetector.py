import cv2
import numpy as np
import pandas as pd

fast = cv2.FastFeatureDetector_create(threshold=25, nonmaxSuppression=True)

#Feature detection parameters
feature_params = dict( maxCorners = 150,
                       qualityLevel = 0.3,
                       minDistance = 2,
                       blockSize =13
                       # useHarrisDetector =True
                       )

fl = pd.read_csv('./depth025.txt',header=None, delim_whitespace=True)
rgb =cv2.imread('./rbg025.jpg')
frame = np.array(fl.values)

nearpoints = np.isfinite(frame)
farpoints = np.isnan(frame)


frame *=(255/20)
frame[np.isnan(frame)] = -1
frame *=-1
img = np.array(frame.astype(np.uint8)).copy()

grey = cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
mask = np.ones(np.shape(grey))
mask[farpoints]=0
mask = mask.astype(np.uint8)

# p0 = cv2.goodFeaturesToTrack(img, mask=None, **feature_params)
# pGrey = fast.detect(grey[farpoints])
pGrey = cv2.goodFeaturesToTrack(grey, mask=mask, **feature_params)
rgb[farpoints] =0
for i in range(int(len(pGrey))):
    a, b = pGrey[i].ravel()
    rgb = cv2.circle(rgb, (a, b), 5, (0, 120, 255))
cv2.imshow('color',rgb)

cv2.waitKey(0)
cv2.destroyAllWindows()
