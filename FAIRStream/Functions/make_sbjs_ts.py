import pandas as pd
from Functions.get_df_raw_from_csv import *
from Functions.fix_df_raw import *
from Functions.agg_df_fix import *


def make_sbjs_ts(df_sample_info, variable_dict, time_resolution, viz=False):
    
    df_sbjs_ts = pd.DataFrame()
    
    for source_key in list(df_sample_info['source_key'].unique()):
        
        # dataframe to store merged data for current source (if there are multiple sources)
        df_src_merged = None
        
        for file_key in list(df_sample_info['file_key'].unique()):

            # get stacked raw df (cohort-wise)
            df_raw = get_df_raw_from_csv(variable_dict, df_sample_info, source_key, file_key, viz=viz)

            # fix current raw file (cohort-wise)
            df_fix = fix_df_raw(variable_dict, df_raw, source_key)

            # aggregate by time resolution (cohort-wise)
            df_agg = agg_df_fix(variable_dict, df_fix, time_resolution)
            
            
            # append file key to variable names 
            suf_vars = [var for var in variable_dict.keys() if var not in ['__uid','__time','__anchor']]
            df_agg_org = df_agg[list(set(df_agg.columns)-set(suf_vars))]
            df_agg_suf  = df_agg[list(set(df_agg.columns).intersection(set(suf_vars)))].add_suffix('___'+str(file_key))
            df_agg = pd.concat([df_agg_org,df_agg_suf],axis=1)
            # merge multiple files
            if df_src_merged is None: #  first df_agg from current source
                df_src_merged = df_agg
                continue
            else:
                if '__time_bin' in df_agg.columns and '__time_bin' in df_src_merged.columns:
                    df_src_merged = pd.merge(left=df_src_merged, right=df_agg,
                                            left_on=['__uid','__time_bin'], right_on=['__uid','__time_bin'], how='outer',
                                            suffixes=('', '___right'),
                                            copy=False)
                else:
                    df_src_merged = pd.merge(left=df_src_merged, right=df_agg,
                                            left_on=['__uid'], right_on=['__uid'], how='left',
                                            suffixes=('', '___right'),
                                            copy=False)    
                
                df_src_merged = df_src_merged.drop(columns=df_src_merged.columns[df_src_merged.columns.str.endswith("___right")].to_list())
                       
        df_sbjs_ts = pd.concat([df_sbjs_ts, df_src_merged],sort=False)
    
    return df_sbjs_ts
