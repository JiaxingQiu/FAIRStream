
from Functions.make_sample_info_from_csv import *
from Functions.make_sbjs_ts import *
from Functions.make_episodes_ts import *
from Functions.viz_episode_ts import *

def make_mvts_df_from_csv_pool(csv_pool_dir, nsbj, frac,source_dict, variable_dict, input_time_len, output_time_len, time_resolution, time_lag, anchor_gap, stratify_by=None, itered=False, viz=False, viz_ts=False):
    
    df_sample_info = make_sample_info_from_csv(csv_pool_dir=csv_pool_dir, source_dict=source_dict, variable_dict=variable_dict, nsbj=nsbj, frac=frac, stratify_by=stratify_by)
    df_sbjs_ts = make_sbjs_ts(df_sample_info, variable_dict, time_resolution, viz=viz) # patient subset dataframe table
    if 'factor' in variable_dict['__anchor'].keys():
        if '__anchor_____1' not in df_sbjs_ts.columns:
            if itered:
                return 'Warning: anchor must have at least 1 level.'
            itered=True
            print("--- System is resampling and will exit after 1 iteration.")
            make_mvts_df_from_csv_pool(csv_pool_dir, nsbj, frac, source_dict, variable_dict, input_time_len, output_time_len, time_resolution, time_lag, anchor_gap, stratify_by=stratify_by, itered=itered, viz=viz, viz_ts=viz_ts)
        
    if viz:
        fig_title = "Visualize Cleaned DataFrame"
        viz_df_hist(df_sbjs_ts, fig_title)

    df_episodes_ts = make_episodes_ts(df_sbjs_ts, variable_dict, input_time_len, output_time_len, time_resolution, time_lag, anchor_gap)
    
    if viz:
        fig_title = "Visualize Episode DataFrame"
        viz_df_hist(df_episodes_ts, fig_title)
    if viz_ts:
        fig_title = "Visualize Episode Data Variables over Time"
        viz_episode_ts(df_episodes_ts, fig_title)
    return df_episodes_ts
