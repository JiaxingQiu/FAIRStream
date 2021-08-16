import pandas as pd
import numpy as np


def make_episodes_ts(df_sbjs_ts, variable_dict, input_time_len, output_time_len, time_resolution, time_lag, anchor_gap):
    """ Summary: make a data frame of stacked episode time sequences
    
    Arges:

    Returns:

    Raises:

    """
 
    # factor type anchor
    if 'factor' in variable_dict['__anchor'].keys():
        for order in variable_dict['__anchor']['factor']['levels'].keys():
            if order == '__1':
                df_sbjs_ts['__anchor'] = df_sbjs_ts['__anchor_____1']
            if '__anchor___'+order in df_sbjs_ts.columns:
                df_sbjs_ts.loc[df_sbjs_ts['__anchor___'+order]==1, ['__anchor']] = int(order.split('__')[-1])
            else:
                print("--- No anchor order " +str(order)+ " found in sampled cohort" )

    
    df_sbjs_ts = df_sbjs_ts.drop(columns=df_sbjs_ts.columns[df_sbjs_ts.columns.str.startswith("__anchor___")].to_list())
    
    df_episodes_ts = pd.DataFrame() # data frame to keep all episodes chunks from the same subject
    for uid in list(set(df_sbjs_ts['__uid'])):

        # get one sbject's dataframe 
        df_sbj_ts = df_sbjs_ts[df_sbjs_ts['__uid']== uid].copy()
        df_sbj_ts = df_sbj_ts.reset_index(drop = True)
        df_sbj_ts = df_sbj_ts.sort_values(by='__time_bin', ascending=True)

        # imputation for this subject
        for var in df_sbj_ts.columns[~df_sbj_ts.columns.isin(['__uid','__anchor','__time_bin'])]:
            var_dict = var.split('___')[0]
            if variable_dict[var_dict]['unique_per_sbj']:
                if df_sbj_ts[var].first_valid_index() is None:
                    df_sbj_ts[var] = np.nan
                else:
                    df_sbj_ts[var] = df_sbj_ts.loc[df_sbj_ts[var].first_valid_index(), var]
                
        # locate anchors
        df_sbj_output_times = df_sbj_ts.loc[df_sbj_ts.__anchor.notna(),['__anchor','__time_bin']].reset_index(drop = True)
        
        # fix anchors by anchor_gap
        df_sbj_output_times = df_sbj_output_times[np.array(df_sbj_output_times.__time_bin.diff(1).isna())|np.array(df_sbj_output_times.__time_bin.diff(1) >= anchor_gap//time_resolution)].reset_index(drop = True)
        
        for idx in list(df_sbj_output_times.index):

            sbj_y_start_time = df_sbj_output_times.loc[idx,'__time_bin'] - (input_time_len+time_lag)//time_resolution 
            sbj_y_stop_time = df_sbj_output_times.loc[idx,'__time_bin'] + int(np.ceil(output_time_len/time_resolution))
            ts = pd.DataFrame(range(int(sbj_y_start_time), int(sbj_y_stop_time)), columns=['__time_bin'])
            
            df_sbj_episode_ts = pd.merge(left=ts, right=df_sbj_ts, left_on='__time_bin', right_on='__time_bin', how='left', copy = False)
            df_sbj_episode_ts['__uid'] = uid
            rel_start = int(-(input_time_len+time_lag)//time_resolution)
            rel_stop = rel_start + df_sbj_episode_ts.shape[0]
            df_sbj_episode_ts['episode_relative_time'] = list(range(rel_start, rel_stop))#0 included
            df_sbj_episode_ts['episode_relative_time'] = df_sbj_episode_ts['episode_relative_time'] * time_resolution
            df_sbj_episode_ts['episode_order'] = idx + 1
            df_sbj_episode_ts['__anchor'] = df_sbj_output_times.loc[idx,'__anchor']

            for var in df_sbj_episode_ts.columns.to_list():
                var_dict = var.split('___')[0]
                try:
                    if variable_dict[var_dict]['output']: # fulfill dummy factor or numeric outcomes
                        df_sbj_episode_ts[var] = df_sbj_episode_ts.loc[df_sbj_episode_ts[var].first_valid_index(), var]
                except:
                    pass
                try:
                    if variable_dict[var_dict]['unique_per_sbj']:
                        if df_sbj_episode_ts[var].first_valid_index() is None:
                            df_sbj_episode_ts[var] = np.nan
                        else:
                            df_sbj_episode_ts[var] = df_sbj_episode_ts.loc[df_sbj_episode_ts[var].first_valid_index(), var]
                        
                except:
                    pass
                try:
                    f_bins = variable_dict[var_dict]['attr']['impute_per_sbj']['forward']//time_resolution
                    b_bins = variable_dict[var_dict]['attr']['impute_per_sbj']['backward']//time_resolution
                    if f_bins>0:
                        df_sbj_episode_ts[var] = df_sbj_episode_ts[var].fillna(method='ffill',limit=f_bins)
                    if b_bins>0:
                        df_sbj_episode_ts[var] = df_sbj_episode_ts[var].fillna(method='bfill',limit=b_bins)
                except:
                    pass
                    
            df_episodes_ts = pd.concat([df_episodes_ts, df_sbj_episode_ts],sort=False)
            df_episodes_ts = df_episodes_ts.drop(columns=df_episodes_ts.columns[df_episodes_ts.columns.str.startswith("__anchor___")].to_list())
            if 'factor' in variable_dict['__anchor'].keys():
                df_episodes_ts = df_episodes_ts.astype({'__anchor':'int'})
            else:
                df_episodes_ts = df_episodes_ts.astype({'__anchor':'float'})
    
     
    # fix factor variables by order of levels in dictionary 
    for fct_var in [var for var in variable_dict.keys() if "factor" in variable_dict[var].keys() and var not in ['__uid','__anchor', '__time']]:
        orders = list(variable_dict[fct_var]['factor']['levels'].keys())[::-1]# reversed order, severity from high to low
        while len(orders)>1:
            # current highest order column name
            top_col = str(fct_var)+'___'+str(orders[0])
            # left lower levels 
            orders.pop(0)
            lower_cols = [str(fct_var)+'___'+str(o) for o in orders]
            # fix lower levels columns
            for lower_col in lower_cols:
                try:
                    df_episodes_ts.loc[(df_episodes_ts[top_col]==1) & (df_episodes_ts[lower_col]==1), [lower_col]]=0
                    print('--- fix order of level: '+lower_col)
                except:
                    pass



    return df_episodes_ts
