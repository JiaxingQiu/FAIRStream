import pandas as pd
import os
from Functions.fix_df_raw import *


def make_sample_info_from_csv(csv_pool_dir, source_dict, variable_dict, nsbj=None, frac=0.3, stratify_by=None):
    
    sep = "_"
    # Find all files in a directory with extension .csv in Python
    df_file_dict = pd.DataFrame()
    df_file_dict['filename'] = os.listdir(csv_pool_dir)
    df_file_dict = df_file_dict[df_file_dict['filename'].str.endswith('.csv')].reset_index(drop=True)
    df_file_dict['fullname'] = csv_pool_dir + '/' + df_file_dict['filename'].astype(str)
    df_file_dict["source_key"] = df_file_dict['filename'].str.split(sep,expand=True).loc[:,0]
    df_file_dict["file_key"] = df_file_dict['filename'].str.split(sep,expand=True).loc[:,2].str.split(".",expand=True).loc[:,0]
    df_file_dict["id"] = df_file_dict['filename'].str.split(sep,expand=True).loc[:,1]
    df_file_dict["__uid"] = df_file_dict['filename'].str.split(sep,expand=True).loc[:,0] + '_' + df_file_dict['filename'].str.split(sep,expand=True).loc[:,1]
    
    # get overlapping source from one cohort
    file_key_base = df_file_dict["file_key"].value_counts(ascending=True).index[0] 
    NSBJ = df_file_dict[df_file_dict["file_key"]==file_key_base].loc[:,"__uid"].nunique()
    
    # filter filenames to include in source dict
    files_include = [file for source in source_dict.keys() for file in source_dict[source].keys() if source_dict[source][file]['include'] ]
    df_file_dict = df_file_dict[df_file_dict['file_key'].isin(files_include)]
    
    if stratify_by is None:
        stratify_by_list = []
    else:
        stratify_by = list(stratify_by)
        stratify_by_list = [var for var in stratify_by if 'factor' in variable_dict[var].keys()]
        print("--- Stratify sampling by :" + str(stratify_by_list))
    
    if len(stratify_by_list)==0:
        if nsbj is not None:
            frac = min(int(nsbj),int(NSBJ)) / NSBJ
        uid_sampled = list(df_file_dict[df_file_dict["file_key"]==file_key_base].loc[:,"__uid"].sample(frac=frac))
        df_sample_info = df_file_dict[df_file_dict["__uid"].isin(uid_sampled)]
    else:
        grouping_df = None
        colnames_dict = []
        stratify_by_list = stratify_by_list+['__uid']
        for var in stratify_by_list:
            colnames_dict = colnames_dict + variable_dict[var]['src_names']
        for source_key in source_dict.keys():
            for file_key in source_dict[source_key].keys():
                fullname = source_dict[source_key][file_key]['path']
                colnames_df = pd.read_csv(str(fullname), index_col=0, nrows=0).columns.tolist()
                usecols = list(set(colnames_df).intersection(set(colnames_dict)))
                if len(usecols)>0:
                    df = pd.read_csv(str(fullname), low_memory=False, usecols=usecols)
                    df = fix_df_raw(variable_dict, df, source_key)
                    df = df.drop_duplicates()
                    if grouping_df is None:
                        grouping_df = df
                    else:
                        keys=list(set(df.columns).intersection(set(grouping_df.columns)))
                        grouping_df = pd.merge(left=grouping_df, right=df, on=keys, how='outer', copy=False)

        if nsbj is not None:
            frac = min(int(nsbj),int(NSBJ)) / NSBJ
        
        G = list(grouping_df.columns[~grouping_df.columns.isin(['__uid','__anchor'])])
        uid_sampled = list(grouping_df.groupby(G)['__uid'].apply(lambda x: x.sample(frac=frac)).reset_index(drop=True))
        df_sample_info = df_file_dict[df_file_dict["__uid"].isin(list(uid_sampled))]  
        
        print("Sucess!  " + str(uid_sampled)+" out of " + str(NSBJ) + " subjects are sampled!")
    return df_sample_info
