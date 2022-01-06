import pandas as pd
import os

def init_csv_fullname_ls(csv_pool_dir, sep = "_"):

    # Find all files in a directory with extension .csv in Python
    df_file_dict = pd.DataFrame()
    df_file_dict['filename'] = os.listdir(csv_pool_dir)
    df_file_dict = df_file_dict[df_file_dict['filename'].str.endswith('.csv')].reset_index(drop=True)
    df_file_dict['fullname'] = csv_pool_dir + '/' + df_file_dict['filename'].astype(str)
    df_file_dict["source_key"] = df_file_dict['filename'].str.split(sep,expand=True).loc[:,0]
    df_file_dict["file_key"] = df_file_dict['filename'].str.split(sep,expand=True).loc[:,2].str.split(".",expand=True).loc[:,0]
    df_file_dict["id"] = df_file_dict['filename'].str.split(sep,expand=True).loc[:,1]
    df_file_dict["__uid"] = df_file_dict['filename'].str.split(sep,expand=True).loc[:,0] + '_' + df_file_dict['filename'].str.split(sep,expand=True).loc[:,1]
    df_file_dict["already_sampled"] = 0

    return df_file_dict