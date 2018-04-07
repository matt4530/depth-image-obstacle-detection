import pandas as pd
import numpy as np
from pandas2arff import pandas2arff as parff
import glob, os, json, sys, cv2


# globals, cached 
classification = ""
feature_params = dict( maxCorners = 150, qualityLevel = 0.3, minDistance = 2, blockSize =13)

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
# TODO: Cache the mask array



def mask(df):
    return np.ma.masked_invalid(df.values)

def average_depth(df): 
    return mask(df).mean()

def median_depth(df): 
    return np.ma.median(mask(df))

def minimum_depth(df): 
    return mask(df).min()
    
def standard_deviation(df):
    return mask(df).std()
    
def points_closer_than_5(df):
    return mask(df[df <= 5]).count()

def detect_blobs(df, rgb_file_name):
    depth = np.array(df.values)
    rgb = cv2.imread(rgb_file_name)
    farpoints = np.isnan(depth)
    grey = cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
    mask = np.ones(np.shape(grey))
    mask[farpoints] = 0
    mask = mask.astype(np.uint8)
    detector = cv2.SimpleBlobDetector_create(params)
    kp = detector.detect(grey)
    #filtering out the keypoints by depth > 20
    kpList = []
    kpAreas = []
    for i in range(len(kp)):
        if mask[int(kp[i].pt[1]),int(kp[i].pt[0])] !=0:
            kpList.append(kp[i])
            kpAreas.append(kp[i].size)
    return kpList, np.array(kpAreas)



def detect_features(df, rgb_file_name):
    frame = np.array(df.values)
    farpoints = np.isnan(frame)

    rgb = cv2.imread(rgb_file_name)
    grey = cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
    mask = np.ones(np.shape(grey))
    mask[farpoints]=0
    mask = mask.astype(np.uint8)

    return cv2.goodFeaturesToTrack(grey, mask=mask, **feature_params)

def features_closer_than_5(points, df):
    # print points
    count = 0
    for x in points:
        x, y = x.ravel()
        if df[x][y] <= 5:
            count += 1
    return count
        

def get_file_features(file_name, rgb_file_name):
    head, tail = os.path.split(file_name)
    print "Prepping " + repr(tail) # + repr(rgb_file_name)
    file_dataframe = pd.read_csv(file_name, header=None, delim_whitespace=True)

    detected_points = detect_features(file_dataframe, rgb_file_name)
    blob_points, blob_areas = detect_blobs(file_dataframe,rgb_file_name)
    #we can sum the total blob areas, average, or we can lots of small ones
    

    return {
        'average_depth': average_depth(file_dataframe),
        'median_depth': median_depth(file_dataframe),
        'minimum_depth': minimum_depth(file_dataframe),
        'standard_deviation': standard_deviation(file_dataframe),
        'closer_than_5': points_closer_than_5(file_dataframe),
        'corners': detected_points.size / 2,
        'corners_closer_than_5': features_closer_than_5(detected_points, file_dataframe),
        'number_of_blobs': len(blob_points),
        'total_blob_area': np.sum(blob_areas),
        'average_blob_size': np.average(blob_areas)
        'class': get_classification(tail)
    }

def get_classification(file_name):
    # print "Getting classification with " + tail
    return classification[file_name]

def get_all_file_features(file_name_list):
    # preallocated for performance efficiency
    final_dataframe = pd.DataFrame(
        index=np.arange(0, len(file_name_list)), 
        columns = (
            'average_depth',
            'median_depth', 
            'minimum_depth', 
            'standard_deviation', 
            'closer_than_5', 
            'corners',
            'corners_closer_than_5',
            'number_of_blobs',
            'total_blob_area',
            'average_blob_size',
            'class'
        )
    )
    
    for i in np.arange(0, len(file_name_list)):
        final_dataframe.loc[i] = get_file_features(file_name_list[i][0], file_name_list[i][1])
    
    return final_dataframe

def all_file_features_to_arff(arff_file_name, file_name_list):
    parff(get_all_file_features(file_name_list), arff_file_name)





# when run from the command line
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Invalid command line paramters.'
        sys.exit()
    arff_file_name = sys.argv[1]
    csv_folder = sys.argv[2]


    all_files = []
    os.chdir(csv_folder)
    for file in glob.glob("*.txt"):
        depth_file = csv_folder + file
        rgb_file = csv_folder + file.replace("depth", "rbg").replace("txt", "jpg")
        all_files.append( (depth_file, rgb_file) )

    classification = json.load(open(csv_folder + 'classifications.json'))

    all_file_features_to_arff(arff_file_name, all_files)
    
    print 'All file data saved to:' + arff_file_name