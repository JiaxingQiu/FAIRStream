import numpy as np
import pandas as pd
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
    
    # remove rows that have not finite values in __time or __uid
    tim_col = list(set(variable_dict['__time']['src_names'])&set(df_raw.columns))
    df_raw = df_raw.loc[np.array(~df_raw[tim_col].isin([np.nan,np.inf,-np.inf]))[:,0],:]
    id_col = list(set(variable_dict['__uid']['src_names'])&set(df_raw.columns))
    df_raw = df_raw.loc[np.array(~df_raw[id_col].isin([np.nan,np.inf,-np.inf]))[:,0],:]
    
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
              
        # replace infinite values with nan
        try:
            df_raw.loc[~np.isfinite(df_raw[var]),var] = np.nan
        except:
            pass
        
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
                upper = np.nanmax(df_raw[var])
                if variable_dict[var]['numeric']['cutoff']['quantile_max'] is not None:
                    upper = np.nanmin([upper, np.nanquantile(df_raw[var], float(variable_dict[var]['numeric']['cutoff']['quantile_max']))] )
                if variable_dict[var]['numeric']['cutoff']['value_max'] is not None:
                    upper = np.nanmin([upper, float(variable_dict[var]['numeric']['cutoff']['value_max'])])
                df_raw.loc[df_raw[var]>upper,[var]] = upper 
                print("--- fix upper boundary for " + str(var) + " by " + str(upper))
            except:
                print("--- fix upper boundary for " + str(var) + " --- failed.")
            try:
                lower = np.nanmin(df_raw[var])
                if variable_dict[var]['numeric']['cutoff']['quantile_min'] is not None:
                    lower = np.nanmax([lower, np.nanquantile(df_raw[var], float(variable_dict[var]['numeric']['cutoff']['quantile_min']))])
                if variable_dict[var]['numeric']['cutoff']['value_min'] is not None:
                    lower = np.nanmax([lower, float(variable_dict[var]['numeric']['cutoff']['value_min'])])
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
            # fix invalid levels (levels not in dictionary) by imputation nan
            outdict_levels = list(set(df_raw[var])-set(variable_dict[var]['factor']['levels'].keys()))
            if len(outdict_levels) != 0: # if number of levels exceed nlevel_max_per_sbj, fix factor var's level limit (including y outcome var)
                print("--- fix out-of-dictionry level/orders " + str(outdict_levels) + " with ['"+str(variable_dict[var]['factor']['impute_per_sbj']['nan_level'])+"']")
                df_raw.loc[np.array(df_raw[var].isin(outdict_levels)),[var]] = variable_dict[var]['factor']['impute_per_sbj']['nan_level']

            #  there got to be a way to fix factor variables faster
            if variable_dict[var]['unique_per_sbj']:
                # add numeric level order 
                level_list = list(variable_dict[var]['factor']['levels'].keys())
                level_df = pd.DataFrame({"level_name":level_list, "level_rank":list(range(len(level_list)))})
                df_raw['level_name'] = df_raw[var]
                df_raw = df_raw.merge(level_df, left_on = "level_name", right_on="level_name")
                # calculate highest fector level within cluster
                max_df = df_raw.groupby(['__uid'])["level_rank"].agg(['max']).reset_index(drop=False)
                df_raw = df_raw.merge(max_df, left_on = "__uid", right_on="__uid")
                df_raw = df_raw.loc[:,list(set(df_raw.columns)-set(['level_name','level_rank']))]
                df_raw = df_raw.merge(level_df, left_on="max", right_on="level_rank")
                df_raw[var] = df_raw['level_name']
                df_raw = df_raw.loc[:,list(set(df_raw.columns)-set(['level_name','level_rank','max']))]
            

            # # fix subject-wise factor attributes
            # for __uid in list(set(df_raw['__uid'])):
            #     # # fix invalid levels (levels not in dictionary) by imputation nan
            #     # outdict_levels = list(set(df_raw[df_raw['__uid']==__uid][var])-set(variable_dict[var]['factor']['levels'].keys()))
            #     # if len(outdict_levels) != 0: # if number of levels exceed nlevel_max_per_sbj, fix factor var's level limit (including y outcome var)
            #     #     print("--- fix out-of-dictionry level/orders " + str(outdict_levels) + " with ['"+str(variable_dict[var]['factor']['impute_per_sbj']['nan_level'])+"'] for subject ---" + str(__uid))
            #     #     df_raw.loc[np.array(df_raw['__uid']==__uid) & np.array(df_raw[var].isin(outdict_levels)),[var]] = variable_dict[var]['factor']['impute_per_sbj']['nan_level']
                    
            #     # fix inconsistence 
            #     if variable_dict[var]['unique_per_sbj']: # if factor level should be unique per subject (independent of time)
            #         # use highest order in dictionary
            #         level_order = list(variable_dict[var]['factor']['levels'].keys())
            #         level_order.reverse()
            #         level_invar = list(set(df_raw[df_raw['__uid']==__uid][var])&set(level_order))
            #         level_invar.sort(key = lambda l:level_order.index(l))
            #         df_raw.loc[df_raw['__uid']==__uid, [var]] = level_invar[0]
            #         # df_raw.loc[df_raw['__uid']==__uid, [var]] = df_raw[df_raw['__uid']==__uid][var].value_counts().index[0] # first most frequent level
                
        print("-- " + str(var) + " fixed")
    
    df_fix = df_raw[include_vars]
    
    return df_fix
