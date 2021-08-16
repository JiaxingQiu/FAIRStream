from matplotlib import pyplot as plt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import SimpleImputer
 

def cohort_fillna(df, vars, method=None, fill_value=-333, viz=False):
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
        return "--- Unrecogenized imputation method. original df returned"
    
    df[vars] = imputer.fit_transform(df[vars])
    df_imputed = df.copy() 

    if viz:
        msno.matrix(df_imputed, figsize=[10, 3], fontsize=6)
        plt.show()
    return df_imputed
