import os
from fairstream import FAIRStream


work_dir = os.path.normpath('project1_hourly')
prvt_stream = FAIRStream.FAIRStream(work_dir)
prvt_stream.querier.update_csv_source_dict()
prvt_stream.querier.update_variable_dict()
prvt_stream.engineer.DefineEpisode(
    input_time_len=24, output_time_len=1, time_resolution=1, time_lag=3, anchor_gap=None)
csv_pool_dir = os.path.join(work_dir, 'csv_pool')
train_df, valid_df, train_tfds, valid_tfds = prvt_stream.engineer.BuildMVTS(
    csv_pool_dir, nsbj=10, train_frac=0.8, batch_size=32, impute_input='mean', impute_output='median', return_data=True)
