import pandas as pd
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
        df_fix['__time_bin'] = df_fix['__time']//time_resolution#*time_resolution# bin fixed df by time resolution
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


