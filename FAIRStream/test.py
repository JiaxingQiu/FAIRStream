from numpy.lib.arraysetops import unique
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

import FAIRStream

bsi_stream = FAIRStream.FAIRStream('/Users/jiaxingqiu/Documents/BSI/code/projects/test')
csv_pool_path = '/Users/jiaxingqiu/Documents/BSI/code/projects/csv_pool'
bsi_stream.querier.update_variable_dict()
bsi_stream.engineer.read_variable_dict()

bsi_stream.engineer.DefineEpisode(input_time_len=2*24*60, output_time_len=1, time_resolution=60, time_lag=0)
bsi_stream.engineer.BuildMVTS(csv_pool_path, nsbj=100, valid_frac=0, test_frac=0, batch_size=32, impute_input='median', impute_output='median', dummy_na=False, topn_eps=10)
X_train, Y_train, X_valid, Y_valid, X_test, Y_test = bsi_stream.engineer.ExtractXY(shape_type="2d")
bsi_stream.engineer.info()
