# depth-image-obstacle-detection
Let the machines learn where obstacles are in your depth images.

## CSV to Arff Usage

Must have the [pandas](https://pypi.python.org/pypi/pandas) and [numpy](https://pypi.python.org/pypi/numpy) packages installed.

### Command Line

```bash
python algorithms.py arff_output_file.arff dataset_folder_with_csv_and_rgb_files
```

Example

```bash
python algorithms.py arff_output_file.arff datasets/train/
```

### From Python

```python
from algorithms import all_file_features_to_arff

file_list = ['file1.csv', 'file2.csv', 'file3.csv']

all_file_features_to_arff('arff_file_output.arff', file_list)
```

## Algorithms Examples

```python
import pandas as pd
from algorithms import *

df = pd.read_csv('./tests/data/depth7.csv', header=None)

print 'Average Depth: ' + str(average_depth(df))
print 'Median Depth: ' + str(median_depth(df))
print 'Minimum Depth: ' + str(minimum_depth(df))
print 'Standard Deviation: ' + str(standard_deviation(df))
print 'closer than 5 meters: ' + str(points_closer_than_5(df))
```

