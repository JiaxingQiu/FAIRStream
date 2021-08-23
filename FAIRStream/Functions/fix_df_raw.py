import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import PowerTransformer

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
                print("--- fix variable dtype for " + str(var) + " --- failed.")

            try:
                scaler = None
                # "minmax", "standard", "maxabs", "robust", "rank", "power", "percentile"
                if variable_dict[var]['numeric']['scaler'] == "minmax":
                    scaler = MinMaxScaler()
                    df_raw[var] = scaler.fit_transform(df_raw[[var]])
                elif variable_dict[var]['numeric']['scaler'] == "standard":
                    scaler = StandardScaler()
                    df_raw[var] = scaler.fit_transform(df_raw[[var]])
                elif variable_dict[var]['numeric']['scaler'] == "maxabs":
                    scaler = MaxAbsScaler()
                    df_raw[var] = scaler.fit_transform(df_raw[[var]])
                elif variable_dict[var]['numeric']['scaler'] == "robust":
                    scaler = RobustScaler()
                    df_raw[var] = scaler.fit_transform(df_raw[[var]])
                elif variable_dict[var]['numeric']['scaler'] == "rank":
                    scaler = QuantileTransformer()
                    df_raw[var] = scaler.fit_transform(df_raw[[var]])
                elif variable_dict[var]['numeric']['scaler'] == "power":
                    scaler = PowerTransformer()
                    df_raw[var] = scaler.fit_transform(df_raw[[var]])
                elif variable_dict[var]['numeric']['scaler'] == "percentile":# estimate the percentile 
                    cuts = np.arange(0,1,0.001)
                    scaler = np.nanquantile(df_raw[var],cuts, axis=None)
                    for i in range(1,len(scaler)):
                        df_raw.loc[np.array(df_raw[var]>=scaler[i-1])&np.array(df_raw[var]<scaler[i]), var]=cuts[i-1]
                    
                if scaler is not None: 
                    print("--- "+str(variable_dict[var]['numeric']['scaler'])+" scaling " + str(var) )
                    continue# if scaling is used, no upper / lower boundary will be used

            except:
                print("--- scaling " + str(var) + " --- skipped")
            
            try:
                upper = max(df_raw[var])
                if variable_dict[var]['numeric']['cutoff']['quantile_max'] is not None:
                    upper = min(upper, np.quantile(df_raw[var], float(variable_dict[var]['numeric']['cutoff']['quantile_max'] )))
                if variable_dict[var]['numeric']['cutoff']['value_max'] is not None:
                    upper = min(upper, float(variable_dict[var]['numeric']['cutoff']['value_max']))
                df_raw.loc[df_raw[var]>upper,[var]] = upper 
                print("--- fix upper boundary for " + str(var) + " by " + str(upper))
            except:
                print("--- fix upper boundary for " + str(var) + " --- failed.")
            try:
                lower = min(df_raw[var])
                if variable_dict[var]['numeric']['cutoff']['quantile_min'] is not None:
                    lower = max(lower, np.quantile(df_raw[var], float(variable_dict[var]['numeric']['cutoff']['quantile_min'])))
                if variable_dict[var]['numeric']['cutoff']['value_min'] is not None:
                    lower = max(lower, float(variable_dict[var]['numeric']['cutoff']['value_min']))
                df_raw.loc[df_raw[var]<lower,[var]] = lower 
                print("--- fix lower boundary for " + str(var) + " by " + str(lower))
            except:
                print("--- fix lower boundary for " + str(var) + " --- failed.")

           
        # ---- fix factor variables ----
        if 'factor' in variable_dict[var].keys():
            try:
                df_raw = df_raw.astype({var:'str'}) 
            except:
                print("--- fix variable dtype for " + str(var) + " --- failed.")
            
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
                    print("--- fix out-of-dictionry level/orders --- " + str(outdict_levels) + "--- with NA for subject ---" + str(__uid))
    
    
    df_fix = df_raw[include_vars]
    
    return df_fix
