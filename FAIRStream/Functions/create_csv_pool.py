import pandas as pd

def create_csv_pool(csv_source_dict, variable_dict, csv_pool_dir, source_key=None, file_key=None, sep = '---', skip_first_col=False):
    
    if source_key is None and file_key is None: # create csv pool for all source files
        for source_key in csv_source_dict.keys():
            for file_key in csv_source_dict[source_key].keys():
                path = csv_source_dict[source_key][file_key]["path"]
                include = csv_source_dict[source_key][file_key]["include"]

                if not include: # skip source file not to include
                    print("--- Skip file : "+str(source_key) +" --- "+ str(file_key) + ". To include, set 'input'=True in csv_source_dict.json ")
                    continue
                if skip_first_col: 
                    all_src_names = pd.read_csv(path, index_col=0, nrows=0).columns.tolist()# only read colume names to check keys
                else:
                    all_src_names = pd.read_csv(path, nrows=0).columns.tolist()# only read colume names to check keys
                __uid_src_names = variable_dict['__uid']['src_names']
                __uid_src_name = list(set(all_src_names).intersection(set(__uid_src_names)))
                if len(__uid_src_name) != 1:
                    print("--- Zero or more than one column for __uid found in: "+str(path))
                    continue
                else:
                    df_src = pd.read_csv(path, low_memory=False)
                for id in list(df_src[__uid_src_name[0]].unique()):
                    df_sbj = df_src[df_src[__uid_src_name[0]]==id]
                    df_sbj.to_csv(str(csv_pool_dir)+'/'+str(source_key)+sep+str(id)+sep+str(file_key)+'.csv', index=False)
    
    else: # only update specified source file to csv pool fle 
        path = csv_source_dict[source_key][file_key]["path"]
        include = csv_source_dict[source_key][file_key]["include"]

        if not include: # skip source file not to include
            print("--- Skip : "+str(source_key) +" --- "+ str(file_key) + ". To include, set 'input'=True in csv_source_dict.json ")
            return
        if skip_first_col: 
            all_src_names = pd.read_csv(path, index_col=0, nrows=0).columns.tolist()# only read colume names to check keys
        else:
            all_src_names = pd.read_csv(path, nrows=0).columns.tolist()# only read colume names to check keys
        __uid_src_names = variable_dict['__uid']['src_names']
        __uid_src_name = list(set(all_src_names).intersection(set(__uid_src_names)))
        if len(__uid_src_name) != 1:
            print("--- Zero or more than one column for __uid found in: "+str(path))
            return
        else:
            df_src = pd.read_csv(path, low_memory=False)
        for id in list(df_src[__uid_src_name[0]].unique()):
            df_sbj = df_src[df_src[__uid_src_name[0]]==id]
            df_sbj.to_csv(str(csv_pool_dir)+'/'+str(source_key)+sep+str(id)+sep+str(file_key)+'.csv', index=False)

    print('Success! The csv pool is ready in dir -- ' + csv_pool_dir)

