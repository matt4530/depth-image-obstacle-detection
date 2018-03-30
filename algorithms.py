import pandas as pd
import numpy as np
from pandas2arff import pandas2arff as parff
import sys

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
    return df[df <= 5].count()

def get_file_features(file_name):
    file_dataframe = pd.read_csv(file_name, header=None)
    
    return {
        'average_depth': average_depth(file_dataframe),
        'median_depth': median_depth(file_dataframe),
        'minimum_depth': minimum_depth(file_dataframe),
        'standard_deviation': standard_deviation(file_dataframe),
        # this function does not currently return a single value but a matrix
        # 'closer_than_5': points_closer_than_5(file_dataframe)
    }

def get_all_file_features(file_name_list):
    # preallocated for performance efficiency
    final_dataframe = pd.DataFrame(index=np.arange(0, len(file_name_list)), columns = ('average_depth', 'median_depth', 'minimum_depth', 'standard_deviation'))
    
    for i in np.arange(0, len(file_name_list)):
        final_dataframe.loc[i] = get_file_features(file_name_list[i])
    
    return final_dataframe

def all_file_features_to_arff(arff_file_name, file_name_list):
    parff(get_all_file_features(file_name_list), arff_file_name)

# when run from the command line
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print '\x1b[1m\x1b[31mERROR:\x1b[22mInvalid command line paramters.\x1b[0m'
        sys.exit()
    arff_file_name = sys.argv[1]
    csv_file_list = sys.argv[2:]
    all_file_features_to_arff(arff_file_name, csv_file_list)
    
    print '\x1b[32mAll file data saved to:\x1b[0m \x1b[1m' + arff_file_name + '\x1b[0m'