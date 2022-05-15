import pandas as pd
import numpy as np
from Functions.viz_df_hist import viz_df_hist

def get_df_raw_from_csv(variable_dict, df_sample_info, source_key, file_key, viz=False, df_raw=None):
    """ 
    
    Usage: 
        read subject-wise csv files from pool by sampling information 

    Arges:
        df_sample_info: dataframe containing information of sampled subjects
        source_key: key of source/cohort in source dictionary
        file_key: key of file location in source dictionary

    Returns:
        df_raw = concated dataframe of raw csv data from multiple files

    """
    
    # find raw variable names in dictionary that are set to be included # variable selection
    colnames_dict = []
    for var in variable_dict.keys():
        if var.startswith('__'):
            colnames_dict = colnames_dict + variable_dict[var]['src_names']
        elif 'input' in variable_dict[var].keys():
            if variable_dict[var]['input']: # if input: true, the variable is the ML predictor, will be kept in both df and tfds
                colnames_dict = colnames_dict + variable_dict[var]['src_names']
            else: # if input: false, the variable is not the ML predictor, but should be engineered and kept in df
                colnames_dict = colnames_dict + variable_dict[var]['src_names']
        elif 'output' in variable_dict[var].keys():
            if variable_dict[var]['output']: # if output: true, the variable is the ML response, will be kept in both df and tfds
                colnames_dict = colnames_dict + variable_dict[var]['src_names']
            else: # if output: false, the variable is not the ML response, but should be engineered and kept in df
                colnames_dict = colnames_dict + variable_dict[var]['src_names']

    if df_raw is None:
        df_raw = pd.DataFrame()
        # loop through all subjects csvs of this file key
        for fullname in list(df_sample_info.loc[np.array(df_sample_info['source_key']==source_key) & np.array(df_sample_info["file_key"]==file_key), 'fullname']):
            colnames_df = pd.read_csv(str(fullname), nrows=0).columns.tolist()# only read colume names row
            usecols = list(set(colnames_df).intersection(set(colnames_dict)))# intersect columns exist in variable dictionary
            df = pd.read_csv(str(fullname), low_memory=False, usecols=usecols)# read selected columns only
            df_raw = pd.concat([df_raw,df])
    else:
        colnames_df = df_raw.columns.tolist()# only read colume names row
        usecols = list(set(colnames_df).intersection(set(colnames_dict)))# intersect columns exist in variable dictionary
        df_raw = df_raw.loc[:,usecols].copy()

    if viz:
        fig_title = "Visualize Raw Dataframe from --- " + str(source_key) + " --- "+ str(file_key)
        viz_df_hist(df_raw, fig_title)
    return df_raw

