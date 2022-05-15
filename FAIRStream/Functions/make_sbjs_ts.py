import pandas as pd
from Functions.get_df_raw_from_csv import *
from Functions.fix_df_raw import *
from Functions.agg_df_fix import *


def make_sbjs_ts(df_sample_info, variable_dict, time_resolution, viz=False, dummy_na=False, df_raw=None):
    
    df_sbjs_ts = pd.DataFrame()
    
    for source_key in list(df_sample_info['source_key'].unique()):
        
        # dataframe to store merged data for current source (if there are multiple sources)
        df_src_merged = None
        
        for file_key in list(df_sample_info['file_key'].unique()):

            # get stacked raw df (cohort-wise)
            df_raw = get_df_raw_from_csv(variable_dict, df_sample_info, source_key, file_key, viz=viz, df_raw=df_raw)

            # fix current raw file (cohort-wise)
            df_fix = fix_df_raw(variable_dict, df_raw, source_key)

            # aggregate by time resolution (cohort-wise)
            df_agg = agg_df_fix(variable_dict, df_fix, time_resolution)
            
            
            # append file key to variable names 
            suf_vars = [var for var in variable_dict.keys() if var not in ['__uid','__time','__anchor']]
            df_agg_org = df_agg[list(set(df_agg.columns)-set(suf_vars))]
            df_agg_suf  = df_agg[list(set(df_agg.columns).intersection(set(suf_vars)))]#.add_suffix('___'+str(file_key))
            redun_cols = list(set(df_agg_org.columns).intersection(set(df_agg_suf.columns)))
            if len(redun_cols) > 0:
                for redun_col in redun_cols:
                    df_redun = pd.concat([df_agg_org[redun_col],df_agg_suf[redun_col]],axis=1)
                    df_agg_org[redun_col] = df_redun.iloc[:,0:2].mean(axis=1)
                    df_agg_suf = df_agg_suf.drop([redun_col], axis=1)
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
        
    # np.nan intruduced by merging
    fct_vars = [var for var in variable_dict.keys() if "factor" in variable_dict[var].keys()]

    for var in fct_vars:
        # if "input" in list(variable_dict[var].keys()):
        #     if not variable_dict[var]['input']: 
        #         continue
        # if "output" in list(variable_dict[var].keys()):
        #     if not variable_dict[var]['output']: 
        #         continue
        # get the nan level name from dictionary and make the col name
        nan_colname = str(var) +"___"+ str(variable_dict[var]['factor']['impute_per_sbj']['nan_level'])
        #  if nan level is set to be merged into any level of the factor variable (e.g. nan is count as level 0)
        if nan_colname in df_sbjs_ts.columns.tolist():
            df_sbjs_ts.loc[df_sbjs_ts[nan_colname].isnull(),[nan_colname]]=1.0
        # if nan level is new
        else:
            # check whether or not the user want to have a seperate column for nan indicator
            if dummy_na:
                # create a seperate column for nan
                df_sbjs_ts[nan_colname]=0.0
                # indicate nan status in nan_colname
                df_sbjs_ts.loc[df_sbjs_ts[str(var) +"___"+ str(list(variable_dict[var]['factor']["levels"].keys())[0]) ].isnull(),[nan_colname]]=1.0
        # fill na of the rest columns by 0
        fillna_cols = [col for col in df_sbjs_ts if col.startswith(var)]
        df_sbjs_ts[fillna_cols] = df_sbjs_ts[fillna_cols].fillna(0)
    
    return df_sbjs_ts
