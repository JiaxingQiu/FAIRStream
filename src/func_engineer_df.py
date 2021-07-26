import numpy as np
import pandas as pd

def viz_df_hist(df, fig_title=None, ncol=3):
    import matplotlib.pyplot as plt 
    if fig_title is None:
        fig_title = "Visualize DataFrame"

    var_list = df.columns[~df.columns.isin(['__uid'])]
    N = int(max(len(var_list),1))
    fig_ncol = int(max(ncol,2))
    fig_nrow = int(np.ceil(N / fig_ncol))
    fig, axs = plt.subplots(fig_nrow, fig_ncol, figsize=(5*(fig_ncol+1), 5*fig_nrow)) # width, height
    axs = axs.flatten()
    
    for i, var in enumerate(var_list):
        try:
            df[str(var)].plot(kind='hist', bins=33, ax=axs[i])
            axs[i].set_xlabel(str(var))
        except:
            try:
                df[str(var)].value_counts().plot(kind='hist', ax=axs[i])
                axs[i].set_xlabel(str(var))
            except:
                axs[i].set_xlabel("Error plot "+str(var))
                pass
            
    fig.suptitle(str(fig_title),fontsize=16) 
    plt.show()

def viz_episode_ts(df, fig_title=None):  
    import matplotlib.pyplot as plt 
    if fig_title is None:
        fig_title = "Visualize Episode DataFrame"
 
    # if time series viz is possible
    if ("episode_relative_time" in df.columns.tolist()) and ("y" in df.columns.tolist()) and ('episode_order' in df.columns.tolist()):
        import seaborn as sns
        sns.set_style('whitegrid')
        var_list = df.columns[~df.columns.isin(['__uid', 'time', '__time_bin','y', 'episode_relative_time', 'episode_order' ])]
        
        for var in var_list:
            fig, axs = plt.subplots(1, 3, figsize=(5*(3+1), 5*1), sharey='row') # width, height
            axs = axs.flatten()
            try:
                sns.lineplot(x='episode_relative_time',y=str(var), data=df, ax=axs[0])
                axs[0].set_ylabel(str(var))
                axs[0].set_xlabel('episode (all) relative time')
            except:
                axs[0].set_xlabel("Error plot "+str(var)+" over episode relative time")
                pass
            
            try: 
                sns.lineplot(x='episode_relative_time',y=str(var), hue='y', data=df, ax=axs[1])
                axs[1].set_xlabel('episode (all) relative time')
            except:
                axs[1].set_xlabel("Error plot "+str(var))
                pass

            try: 
                sns.lineplot(x='episode_relative_time', y=str(var), hue='y', data=df[df['episode_order']==1], ax=axs[2])
                axs[2].set_xlabel('episode (1st) relative time')
            except:
                axs[2].set_xlabel("Error plot "+str(var))
                pass
            
            fig.suptitle(str(var)+" Time Series Plots",fontsize=16) 
            plt.show()
                



def get_df_raw_from_csv(variable_dict, df_sample_info, source_key, file_key, viz=False):
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
    df_raw = pd.DataFrame()
    # find raw variable names in dictionary that are set to be included # variable selection
    colnames_dict = []
    for var in variable_dict.keys():
        if var.startswith('__'):
            colnames_dict = colnames_dict + variable_dict[var]['src_names']
        elif 'input' in variable_dict[var].keys():
            if variable_dict[var]['input']:
                colnames_dict = colnames_dict + variable_dict[var]['src_names']
        elif 'output' in variable_dict[var].keys():
            if variable_dict[var]['output']:
                colnames_dict = colnames_dict + variable_dict[var]['src_names']
    
   # loop through all subjects csvs of this file key
    for fullname in list(df_sample_info.loc[np.array(df_sample_info['source_key']==source_key) & np.array(df_sample_info["file_key"]==file_key), 'fullname']):
        colnames_df = pd.read_csv(str(fullname), index_col=0, nrows=0).columns.tolist()# only read colume names row
        usecols = list(set(colnames_df).intersection(set(colnames_dict)))# intersect columns exist in variable dictionary
        df = pd.read_csv(str(fullname), low_memory=False, usecols=usecols)# read selected columns only
        df_raw = pd.concat([df_raw,df])

    if viz:
        fig_title = "Visualize Raw Dataframe from --- " + str(source_key) + " --- "+ str(file_key)
        viz_df_hist(df_raw, fig_title)
    return df_raw


def fix_df_raw(variable_dict, df_raw, source_key):
    """ 
    
    Usage: 
        fix raw dataframe queries from a database by conditions of sample subjects

    Arges:
        df_raw: raw dataframe of a sampled cohort
        source_key: key of source in source dictionary
        file_key: key of file location in source dictionary
        variable_dict: variable dictionary (valid and clean)

    Returns:
        df_fix = fixed dataframe

    """

    include_vars = []
    for var in variable_dict.keys():
        if len(set(variable_dict[var]['src_names']).intersection(set(df_raw.columns.to_list())))==0: # skip variable if not in current dataframe
            continue
        include_vars.append(var) # append to list of all variables to include

        
        # --- fix variable name ---
        src_name = df_raw.columns[df_raw.columns.isin(variable_dict[var]['src_names'])][0]
        if var == '__anchor':
            df_raw[var] = df_raw[src_name]
        else:
            df_raw.rename(columns={src_name:var}, inplace=True)
              
    
        # --- fix __uid ---
        if var == '__uid':
            df_raw = df_raw.astype({var:'str'}) 
            df_raw[var] = source_key+'_'+df_raw[var] 
            continue
        
        # --- fix __time ---
        if var == "__time":
            df_raw = df_raw.astype({var:'int'}) 

        
        # --- fix numeric variables ---
        if 'numeric' in variable_dict[var].keys():
            try:
                df_raw = df_raw.astype({var:'float'}) 
            except:
                print("--- Fix variable dtype for " + str(var) + " --- failed.")
            try:
                upper = max(df_raw[var])
                if variable_dict[var]['numeric']['cutoff']['quantile_max'] is not None:
                    upper = min(upper, np.quantile(df_raw[var], float(variable_dict[var]['numeric']['cutoff']['quantile_max'] )))
                if variable_dict[var]['numeric']['cutoff']['value_max'] is not None:
                    upper = min(upper, float(variable_dict[var]['numeric']['cutoff']['value_max']))
                df_raw.loc[df_raw[var]>upper,[var]] = upper 
                print("--- Fix upper boudary for " + str(var) + " by " + str(upper))
            except:
                print("--- Fix upper boundary for " + str(var) + " --- failed.")
            try:
                lower = min(df_raw[var])
                if variable_dict[var]['numeric']['cutoff']['quantile_min'] is not None:
                    lower = max(lower, np.quantile(df_raw[var], float(variable_dict[var]['numeric']['cutoff']['quantile_min'])))
                if variable_dict[var]['numeric']['cutoff']['value_min'] is not None:
                    lower = max(lower, float(variable_dict[var]['numeric']['cutoff']['value_min']))
                df_raw.loc[df_raw[var]<lower,[var]] = lower 
                print("--- Fix lower boudary for " + str(var) + " by " + str(lower))
            except:
                print("--- Fix lower boundary for " + str(var) + " --- failed.")
  
        # ---- fix factor variables ----
        if 'factor' in variable_dict[var].keys():
            try:
                df_raw = df_raw.astype({var:'str'}) 
            except:
                print("--- Fix variable dtype for " + str(var) + " --- failed.")
            
            # unify level name
            for level in variable_dict[var]['factor']['levels'].keys():
                df_raw.loc[df_raw[var].isin(variable_dict[var]['factor']['levels'][level]), [var]] = level
           
            # fix subject-wise factor attributes
            for __uid in list(set(df_raw['__uid'])):
                # fix inconsistence 
                if variable_dict[var]['unique_per_sbj']: # if factor level should be unique per subject (independent of time)
                    df_raw.loc[df_raw['__uid']==__uid, [var]] = df_raw[df_raw['__uid']==__uid][var].value_counts().index[0] # first most frequent level
                # fix invalid levels (levels not in dictionary)
                outdict_levels = list(set(df_raw[df_raw['__uid']==__uid][var])-set(variable_dict[var]['factor']['levels'].keys()))
                if len(outdict_levels) != 0: # if number of levels exceed nlevel_max_per_sbj, fix factor var's level limit (including y outcome var)
                    df_raw.loc[np.array(df_raw['__uid']==__uid) & np.array(df_raw[var].isin(outdict_levels)),[var]] = np.nan
                    print("--- Fix out-of-dictionry level/orders --- " + str(outdict_levels) + "--- with NA for subject ---" + str(__uid))
    
    
    df_fix = df_raw[include_vars]
    
    return df_fix



def agg_df_fix(variable_dict, df_fix, time_resolution):
    
    # take mean for numeric variables
    num_vars = []
    fct_vars = []
    for var in list(df_fix.columns[~df_fix.columns.isin(['__uid','__time'])]):
        if 'numeric' in variable_dict[var].keys():
            num_vars.append(var)
        if 'factor' in variable_dict[var].keys():
            fct_vars.append(var)

    if '__time' in df_fix.columns:
        df_fix['__time_bin'] = df_fix['__time']//time_resolution*time_resolution# bin fixed df by time resolution
        keys = ['__uid','__time_bin']
    else:
        keys = ['__uid']

    if len(num_vars)==0: # aggregate numeric vars by taking the mean
        df_num_agg = df_fix[keys].drop_duplicates()
    else:
        df_num_agg = df_fix.groupby(keys)[num_vars].agg('mean').reset_index()
    
    
    if len(fct_vars)==0:# aggregate dummied factor vars by taking the max 
        df_fct_agg = df_fix[keys].drop_duplicates()
    else: 
        df_fix = pd.get_dummies(df_fix, columns=fct_vars, dtype=int, dummy_na=False, prefix_sep='___')  
        
        dummy_cols = []# aggregate dummy vars by max in a time bin
        for col in list(df_fix.columns):
            if col.split("___")[0] in fct_vars:
                dummy_cols.append(col)
        df_fct_agg = df_fix.groupby(keys)[dummy_cols].agg('max').reset_index()
    df_agg = pd.merge(left=df_num_agg,right=df_fct_agg,on=keys,copy = False)# merge columns together
    
    return df_agg



