import cv2
import numpy as np
import pandas as pd

fl = pd.read_csv('./depth154.txt',header=None, delim_whitespace=True)
rgb =cv2.imread('./rbg154.jpg')
frame = np.array(fl.values)

nearpoints = np.isfinite(frame)
farpoints = np.isnan(frame)
grey = cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
mask = np.ones(np.shape(grey))
mask[farpoints]=0
mask = mask.astype(np.uint8)


# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 1
params.maxThreshold = 255
params.filterByArea = True
params.minArea = 400
params.filterByCircularity = False
params.filterByConvexity = True
params.minConvexity = 0.2
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Create a detector with the parameters
rgb[farpoints] =0
detector = cv2.SimpleBlobDetector_create(params)
kp = detector.detect(grey)

#get rid of far away keypoints
kpList = []
for i in range(len(kp)):
    if mask[int(kp[i].pt[1]),int(kp[i].pt[0])] != 0:
      kpList.append(kp[i])
im_with_keypoints = cv2.drawKeypoints(rgb, kpList, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow('rgb',im_with_keypoints)
#KpList is a list of keypoints. Keypoint is a class containing area and points

cv2.waitKey(0)
cv2.destroyAllWindows()
