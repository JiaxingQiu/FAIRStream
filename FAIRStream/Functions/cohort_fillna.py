from matplotlib import pyplot as plt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import SimpleImputer
import numpy as np
 

def cohort_fillna(refer_df, df, vars, method=None, fill_value=-333, viz=False):
    # refer_df is the one to train the parameters of imputor 
    # df is the target dataframe to impute
    if viz:
        import missingno as msno
        msno.matrix(df, figsize=[10, 3], fontsize=6)
        plt.show()
        
    if method == "mice": # MICE(IterativeImputer)
        imputer = IterativeImputer(random_state=333)
    elif method == "median":
        imputer = SimpleImputer(strategy='median')
    elif method == "mean":
        imputer = SimpleImputer(strategy='mean')
    elif method == "most_frequent":
        imputer = SimpleImputer(strategy='most_frequent')
    elif method == "constant":
        imputer = SimpleImputer(strategy='constant', fill_value=fill_value)
    else:
        print("--- Unrecogenized imputation method. original df returned")
        return df
    
    refer_df[vars] = refer_df[vars].replace([np.inf, -np.inf], np.nan, inplace=False)
    df[vars] = df[vars].replace([np.inf, -np.inf], np.nan, inplace=False)
    
    df_imputed = df.copy() 
    try:
        imputer.fit(refer_df[vars])
        df_imputed[vars] = imputer.transform(df[vars])
    except:
        print("Imputation failed, sample size might be too small.")
        pass
    

    if viz:
        msno.matrix(df_imputed, figsize=[10, 3], fontsize=6)
        plt.show()
    return df_imputed
