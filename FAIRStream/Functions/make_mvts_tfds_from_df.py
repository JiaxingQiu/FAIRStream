from Functions.window_generator import WindowGenerator
import numpy as np

def make_mvts_tfds_from_df(mvts_df, input_vars, output_vars, input_time_len, output_time_len, time_resolution, time_lag, batch_size):
   
    input_vars = list(set(mvts_df.columns).intersection(set(input_vars)))
    output_vars = list(set(mvts_df.columns).intersection(set(output_vars)))
    df = mvts_df.loc[:,mvts_df.columns.isin(input_vars+output_vars)]
    
    input_width = input_time_len//time_resolution
    output_width = int(np.ceil(output_time_len/time_resolution))
    shift = time_lag + output_width
    stride = input_width + shift
    w = WindowGenerator(df, input_width=input_width, output_width=output_width, shift=shift, stride=stride, input_columns=input_vars, output_columns=output_vars)
    tfds = w.make_dataset(batch_size)
    return tfds
