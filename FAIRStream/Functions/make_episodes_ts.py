import pandas as pd
import numpy as np


def make_episodes_ts(df_sbjs_ts, variable_dict, input_time_len, output_time_len, time_resolution, time_lag, anchor_gap, topn_eps=None):
    """ Summary: make a data frame of stacked episode time sequences
    
    Arges:
        topn_eps: maximum episode counts from a single subject, if not none

    Returns:

    Raises:

    """
 
    # factor type anchor
    orders=[]
    if 'factor' in variable_dict['__anchor'].keys():
        orders = list(variable_dict['__anchor']['factor']['levels'].keys())# reversed order, severity from high to low
        for i, order in enumerate(orders):
            if i == 0:
                df_sbjs_ts['__anchor'] = df_sbjs_ts['__anchor___'+str(order)]
            if '__anchor___'+order in df_sbjs_ts.columns:
                df_sbjs_ts.loc[df_sbjs_ts['__anchor___'+order]==1, ['__anchor']] = order
            else:
                print("--- No anchor order " +str(order)+ " found in sampled cohort" )

    df_sbjs_ts = df_sbjs_ts.drop(columns=df_sbjs_ts.columns[df_sbjs_ts.columns.str.startswith("__anchor___")].to_list())

    # prepare variables
    outvars=[]
    unique_vars=[]
    for var in df_sbjs_ts.columns[~df_sbjs_ts.columns.isin(['__uid','__anchor','__time_bin'])]:
        # get variable name in dictionary
        var_dict = var.split('___')[0]
        # find all output variables
        if 'output' in list(variable_dict[var_dict].keys()):
            if variable_dict[var_dict]['output']:
                outvars.append(var)
        # fill missingness caused by merging for unique value vars 
        if variable_dict[var_dict]['unique_per_sbj']:
            unique_vars.append(var)
            

    # data frame to keep all episodes chunks from all subjects
    df_sbjs_eps_ts = pd.DataFrame() 
    for uid in list(set(df_sbjs_ts['__uid'])):
        print("--- prepare episodes for "+str(uid))

        # get one subject's dataframe 
        df_sbj_ts = df_sbjs_ts[df_sbjs_ts['__uid']== uid].copy()
        df_sbj_ts = df_sbj_ts.reset_index(drop = True)
        df_sbj_ts = df_sbj_ts.sort_values(by='__time_bin', ascending=True)

        for var in unique_vars:
            if df_sbj_ts[var].first_valid_index() is None:
                df_sbj_ts[var] = np.nan
            else:
                df_sbj_ts[var] = df_sbj_ts.loc[df_sbj_ts[var].first_valid_index(), var]
        
        # get anchor columns
        df_sbj_output_times = df_sbj_ts[['__anchor','__time_bin']].reset_index(drop = True)
                
        if 'factor' in variable_dict['__anchor'].keys():
            # locate anchors
            df_sbj_output_times = df_sbj_output_times.loc[df_sbj_output_times.__anchor.isin(list(variable_dict['__anchor']['factor']['levels'].keys())),['__anchor','__time_bin']].reset_index(drop = True)
            
            # select anchors based on order of levels in dictionary (e.g. severity)
            orders = list(variable_dict['__anchor']['factor']['levels'].keys())[::-1]# reversed order, severity from high to low
            while len(orders)>0:
                order=orders[0] # current top anchor
                orders.pop(0)# left lower levels 
                upper_anchors = df_sbj_output_times[df_sbj_output_times['__anchor']==order]
                upper_anchors['__ep_order']=upper_anchors.__time_bin//(anchor_gap//time_resolution)
                upper_anchors = upper_anchors[np.array(upper_anchors.__ep_order.diff(1).isna())|np.array(upper_anchors.__ep_order.diff(1) >= 1)]
                # nan invalid anchors
                df_sbj_output_times.loc[np.array(df_sbj_output_times['__anchor']==order)&(np.array(~df_sbj_output_times['__time_bin'].isin(upper_anchors['__time_bin']) )), ['__anchor']]=np.nan

                for idx in list(upper_anchors.index):
                    override_zone_start = int(upper_anchors.loc[idx,['__time_bin']]-anchor_gap//time_resolution) 
                    override_zone_stop = int(upper_anchors.loc[idx,['__time_bin']]+anchor_gap//time_resolution) 
                    # nan invalid anchors
                    df_sbj_output_times.loc[np.array(df_sbj_output_times['__time_bin']>override_zone_start)&(np.array(df_sbj_output_times['__time_bin']<override_zone_stop))&(np.array(df_sbj_output_times['__anchor'].isin(list(orders)))), ['__anchor']]=np.nan      
        
        # get final not na anchors left
        df_sbj_output_times = df_sbj_output_times[~df_sbj_output_times['__anchor'].isna()].reset_index(drop=True)
        
        for ep_order in list(df_sbj_output_times.index):

            # check maximum limits of episodes from a single subject
            if topn_eps is not None and int(topn_eps)>0:
                if ep_order+1 >= int(topn_eps):
                    break # break inner loop

            # current anchor and absolute time bin value
            ep_anchor = df_sbj_output_times.__anchor[ep_order]
            ep_abs_time = df_sbj_output_times.__time_bin[ep_order]

            # for the sake of forward and backward imputation, expand current episode by twice the input ahead and twice the output after
            # relative time sequence in an episode (relative to time 0)
            rel_start = 2*int(-(input_time_len+time_lag)//time_resolution)
            rel_stop = 2*int(np.ceil(output_time_len/time_resolution)) #(2 = (0,1))
            # adjust expanded window to avoid overlapping with previous episode
            rel_start = max(rel_start, int(np.ceil(output_time_len/time_resolution)) - int(anchor_gap//time_resolution))
            rel_stop = min(rel_stop, int(anchor_gap//time_resolution)-int((input_time_len+time_lag)//time_resolution))
            ep_rel_ts = list(range(rel_start, rel_stop))#0 included # episdoe relative time sequence
            
            # absolute time sequence for current episode
            abs_start = ep_abs_time + rel_start
            abs_stop = ep_abs_time + rel_stop
            ep_abs_ts = list(range(int(abs_start), int(abs_stop)))
            assert len(ep_rel_ts) == len(ep_abs_ts), "Relative window length and absolute window length not match!"

            
            # final window start and stop time index
            abs_start_final = ep_abs_time - (input_time_len+time_lag)//time_resolution 
            abs_stop_final = ep_abs_time + int(np.ceil(output_time_len/time_resolution))
            ep_abs_ts_final = list(range(int(abs_start_final), int(abs_stop_final)))
            # assert len(ep_abs_ts) == 2*len(ep_abs_ts_final), "Expended window length for f/b imputation is not twice as large as the final episode length"
            
            # make abs ts a data frame for left merge
            df_ts = pd.DataFrame({'__time_bin':ep_abs_ts})
            
            # data frame for the time sequence of current episode from current subject
            df_sbj_ep_ts = pd.merge(left=df_ts, right=df_sbj_ts, left_on='__time_bin', right_on='__time_bin', how='left', copy = False)
            
            # build up key private columns / variables
            df_sbj_ep_ts['__uid'] = uid
            df_sbj_ep_ts['__ep_relative_time'] = ep_rel_ts
            df_sbj_ep_ts['__ep_relative_time'] = df_sbj_ep_ts['__ep_relative_time'] * time_resolution
            df_sbj_ep_ts['__ep_order'] = ep_order + 1
            df_sbj_ep_ts['__anchor'] = ep_anchor


            # build up input / output (predictor / responce) variables
            for var in df_sbj_ep_ts.columns.to_list():
                # skip private variables
                if var.startswith('__'):
                    continue
                # key var name in the dictionary
                var_dict = var.split('___')[0]
                # filter out invalid input / output variables
                if 'input' in list(variable_dict[var_dict].keys()):
                    if not variable_dict[var_dict]['input']:
                        continue
                elif 'output' in list(variable_dict[var_dict].keys()):
                    if not variable_dict[var_dict]['output']:
                        continue
                else:
                    continue
                
                # imputation for unique per sbj variables
                if variable_dict[var_dict]['unique_per_sbj']:
                    if df_sbj_ts[var].first_valid_index() is None:
                        df_sbj_ep_ts[var] = np.nan
                    else:
                        df_sbj_ep_ts[var] = df_sbj_ts.loc[df_sbj_ts[var].first_valid_index(), var]

                # imputation for factor variables
                if 'factor' in list(variable_dict[var_dict].keys()):
                    # factor variable wihtin one episode should be constantly unique
                    #df_sbj_ep_ts[var] = df_sbj_ep_ts.loc[df_sbj_ep_ts[var].first_valid_index(), var]
                    orders = list(variable_dict[var_dict]['factor']['levels'].keys())[::-1]# reversed order, severity from high to low
                    while len(orders)>0:
                        top_col = str(var_dict)+'___'+str(orders[0])# current highest order column name
                        orders.pop(0)# left lower levels 
                        if len(orders)==0:
                            lower_cols=[]
                        else:
                            lower_cols = [str(var_dict)+'___'+str(o) for o in orders]

                        if any(df_sbj_ep_ts[top_col]==1):
                        # fix lower levels columns if possible (is sample size is small, all episodes from all subjects might only have one level)
                            df_sbj_ep_ts[top_col]=1.0
                            if len(lower_cols)>0:
                                df_sbj_ep_ts[lower_cols]=0.0
                        else:
                            df_sbj_ep_ts[top_col]=0.0


                # imputation for numeric variables
                if 'numeric' in list(variable_dict[var_dict].keys()):
                    f_bins = variable_dict[var_dict]['numeric']['impute_per_sbj']['forward']//time_resolution
                    b_bins = variable_dict[var_dict]['numeric']['impute_per_sbj']['backward']//time_resolution
                    if f_bins>0:
                        df_sbj_ep_ts[var] = df_sbj_ep_ts[var].fillna(method='ffill',limit=f_bins)
                    if b_bins>0:
                        df_sbj_ep_ts[var] = df_sbj_ep_ts[var].fillna(method='bfill',limit=b_bins)
            
            # slice final chunk of the window / episode
            df_sbj_ep_ts = df_sbj_ep_ts[df_sbj_ep_ts['__time_bin'].isin(ep_abs_ts_final)]
                
            # append current episode df to all episodes df of current subject
            df_sbjs_eps_ts = pd.concat([df_sbjs_eps_ts, df_sbj_ep_ts],sort=False)
            df_sbjs_eps_ts = df_sbjs_eps_ts.drop(columns=df_sbjs_eps_ts.columns[df_sbjs_eps_ts.columns.str.startswith("__anchor___")].to_list())
            df_sbjs_eps_ts = df_sbjs_eps_ts.astype({'__anchor':'str'})

        # print output info after concat each uid
        print("Success! Output/responce variable mean in current sample space  --- ")
        print(df_sbjs_eps_ts[outvars].mean(axis=0))

       
    # exclude levels that are not in dictionary for factor output 
    #[var for var in variable_dict.keys() if 'output' in variable_dict[var].keys()]

    return df_sbjs_eps_ts
