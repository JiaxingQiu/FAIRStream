import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from scipy import stats



def cmp_src_csv(source_dict, variable_dict, nrows=None, var_list=None):
    
    # check this study has multiple sources
    if len(source_dict.keys()) <= 1:
        return "less than 2 data sources"
    else:
        if var_list is None:
            var_list = list(variable_dict.keys())
        for var in var_list:
            if "numeric" not in list(variable_dict[var].keys()):
                print("skip non-numeric var: " + var)
                continue
            try:
                var_src_names = variable_dict[var]['src_names']
                var_df_all = pd.DataFrame()
                for source in source_dict.keys():
                    for file in source_dict[source].keys():
                        filepath = source_dict[source][file]["path"]
                        colnames_df = pd.read_csv(str(filepath), index_col=0, nrows=0).columns.tolist() # only read column names 
                        use_col = list(set(colnames_df).intersection(set(var_src_names)))
                        if len(use_col)==0:
                            continue
                        elif len(use_col)>1:
                            print("Error: naming conflict!")
                            continue
                        else:
                            if nrows is None:
                                var_df = pd.read_csv(str(filepath), low_memory=False, usecols=use_col)
                            else:
                                var_df = pd.read_csv(str(filepath), low_memory=False, usecols=use_col, nrows=int(nrows))
                            var_df.rename(columns={use_col[0]:var}, inplace=True)
                            var_df['source'] = source
                            scaler = StandardScaler()
                            var_df[var+'_scaled'] = scaler.fit_transform(var_df[[var]])
                            var_df_all = pd.concat([var_df_all, var_df])
                
                # compare all possible pairs of sources
                valid_src_list = var_df_all['source'].unique().tolist()
                if len(valid_src_list)<2:
                    print(var + ' only comes from one source')
                    continue
                else:
                    while len(valid_src_list)>=2:
                        pair_df = var_df_all[var_df_all['source'].isin(valid_src_list[0:2])]
                        # plot original scale distributions group by source
                        xname=var
                        fig, axs = plt.subplots(1,2,figsize=(13, 5))
                        axs = axs.flatten()
                        sns.histplot(data=pair_df, x=xname, hue="source", multiple="dodge", kde=True, ax=axs[0])
                        axs[0].set_xlabel(xname)
                        axs[0].set_ylabel('density')
                        sns.ecdfplot(data=pair_df, x=xname, hue="source", ax=axs[1])
                        axs[1].set_xlabel(xname)
                        axs[1].set_ylabel('ECDF')
                        arr1 = pair_df[pair_df['source']==valid_src_list[0]][xname].tolist()
                        arr2 = pair_df[pair_df['source']==valid_src_list[1]][xname].tolist()
                        fig.suptitle(str(stats.ks_2samp(arr1, arr2)),fontsize=16) 
                        plt.show(); 
                        # plot original scale distributions group by source
                        xname=var+'_scaled'
                        fig, axs = plt.subplots(1,2,figsize=(13, 5))
                        axs = axs.flatten()
                        sns.histplot(data=pair_df, x=xname, hue="source", multiple="dodge", kde=True, ax=axs[0])
                        axs[0].set_xlabel(xname)
                        axs[0].set_ylabel('density')
                        sns.ecdfplot(data=pair_df, x=xname, hue="source", ax=axs[1])
                        axs[1].set_xlabel(xname)
                        axs[1].set_ylabel('ECDF')
                        arr1 = pair_df[pair_df['source']==valid_src_list[0]][xname].tolist()
                        arr2 = pair_df[pair_df['source']==valid_src_list[1]][xname].tolist()
                        fig.suptitle(str(stats.ks_2samp(arr1, arr2)),fontsize=16) 
                        plt.show(); 
                        valid_src_list.pop(0)
        
            except Exception as ex:
                print("Error comparing var :" +var)
                print(ex)
                pass

