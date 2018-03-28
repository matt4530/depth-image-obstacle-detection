import pandas as pd
import numpy as np

df = pd.read_csv('depth7.csv', header=None)



def mask(df):
    return np.ma.masked_invalid(df.values)

def average_depth(df): 
    return mask(df).mean()

def median_depth(df): 
    return np.ma.median(mask(df))

def minimum_depth(df): 
    return mask(df).min()

#Median Dept: 2.00  - Matt
#Closest Depth: 0.5  - Matt
#Average Depth: 2.14  - Matt
print "Average Depth: " + str(average_depth(df))
print "Median Depth: " + str(median_depth(df))
print "Minimum Depth: " + str(minimum_depth(df))