import pandas as pd
from Functions.fix_df_raw import *


def make_sample_info_from_csv(df_file_dict, source_dict, variable_dict, nsbj=None, frac=0.3, stratify_by=None):
   
    # total number of subjects in the csv pool
    df_file_dict_updated = df_file_dict
    NSBJ = df_file_dict_updated.groupby("source_key").apply(lambda x: x["file_key"].value_counts()[0]).sum()
    
    # filter filenames to include in source dict
    sources_include = [source for source in source_dict.keys() for file in source_dict[source].keys() if bool(source_dict[source][file]['include']) ]
    files_include = [file for source in source_dict.keys() for file in source_dict[source].keys() if bool(source_dict[source][file]['include']) ]
    df_file_dict = df_file_dict_updated[ (df_file_dict_updated['source_key'].isin(sources_include)) & (df_file_dict_updated['file_key'].isin(files_include)) & (df_file_dict_updated['already_sampled']==0)]
    
    #file_key_base = df_file_dict["file_key"].value_counts(ascending=True).index[-1] 
    NSBJ_include = df_file_dict.groupby("source_key").apply(lambda x: x["file_key"].value_counts()[0]).sum()
    
    if stratify_by is None:
        stratify_by_list = []
    else:
        stratify_by = list(stratify_by)
        stratify_by_list = [var for var in stratify_by if 'factor' in variable_dict[var].keys()]
        print("--- Stratify sampling by :" + str(stratify_by_list))
    
    if len(stratify_by_list)==0:
        if nsbj is not None:
            frac = min(int(nsbj),int(NSBJ_include)) / NSBJ_include
        df_uid = pd.DataFrame({"__uid":df_file_dict.loc[:,"__uid"].unique()})
        uid_sampled = list(df_uid.loc[:,"__uid"].sample(frac=frac)) #[df_file_dict["file_key"]==file_key_base]
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
            frac = min(int(nsbj),int(NSBJ_include)) / NSBJ_include
        
        G = list(grouping_df.columns[~grouping_df.columns.isin(['__uid','__anchor'])])
        uid_sampled = list(grouping_df.groupby(G)['__uid'].apply(lambda x: x.sample(frac=frac)).reset_index(drop=True))
        df_sample_info = df_file_dict[df_file_dict["__uid"].isin(list(uid_sampled))]  

    df_file_dict_updated.loc[df_file_dict_updated["__uid"].isin(list(df_sample_info['__uid'])), 'already_sampled'] += 1

    sampling_message = str(len(set(uid_sampled)))+"---out of---" + str(NSBJ_include) + "---subjects are sampled from csv pool of size---" + str(NSBJ)
    print(sampling_message)
    return df_sample_info, df_file_dict_updated, sampling_message
