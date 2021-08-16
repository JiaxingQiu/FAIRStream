import matplotlib.pyplot as plt 
import numpy as np

def viz_df_hist(df, fig_title=None, ncol=3):
    
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
