import matplotlib.pyplot as plt 
import seaborn as sns
sns.set_style('whitegrid')
def viz_episode_ts(df, fig_title=None):  
    
    if fig_title is None:
        fig_title = "Visualize Episode DataFrame"
 
    # if time series viz is possible
    if ("__ep_relative_time" in df.columns.tolist()) and ('__ep_order' in df.columns.tolist()):
        
        var_list = df.columns[~df.columns.isin(['__uid', '__time_bin', '__anchor', '__ep_relative_time', '__ep_order' ])]
        
        for var in var_list:
            fig, axs = plt.subplots(1, 2, figsize=(3*(2+1), 3*1), sharey='row') # width, height
            axs = axs.flatten()
            try:
                sns.lineplot(x='__ep_relative_time',y=str(var), data=df, ax=axs[0])
                axs[0].set_ylabel(str(var))
                axs[0].set_xlabel('episode (all) relative time')
            except:
                axs[0].set_xlabel("Error plot "+str(var)+" over episode relative time")
                pass
            
            try: 
                sns.lineplot(x='__ep_relative_time', y=str(var), data=df[df['__ep_order']==1], ax=axs[1])
                axs[1].set_xlabel('episode (1st) relative time')
            except:
                axs[1].set_xlabel("Error plot "+str(var))
                pass
            
            fig.suptitle(str(var)+" Time Series Plots",fontsize=16) 
            plt.show()
                
