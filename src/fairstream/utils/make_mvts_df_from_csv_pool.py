from sklearn.impute import SimpleImputer
from sklearn.impute import IterativeImputer
# from sklearn.experimental import enable_iterative_imputer
import numpy as np
from matplotlib import pyplot as plt

from utils.engineer_df import *

plt.rcParams.update({'figure.max_open_warning': 0})


def make_sample_info_from_csv(csv_pool_dir, source_dict, variable_dict, nsbj=None, frac=0.3, stratify_by=None):
    import pandas as pd
    import os
    sep = "---"
    # Find all files in a directory with extension .csv in Python
    df_file_dict = pd.DataFrame()
    df_file_dict['filename'] = os.listdir(csv_pool_dir)
    df_file_dict = df_file_dict[df_file_dict['filename'].str.endswith(
        '.csv')].reset_index(drop=True)
    df_file_dict['fullname'] = csv_pool_dir + \
        '/' + df_file_dict['filename'].astype(str)
    df_file_dict["source_key"] = df_file_dict['filename'].str.split(
        sep, expand=True).loc[:, 0]
    df_file_dict["file_key"] = df_file_dict['filename'].str.split(
        sep, expand=True).loc[:, 2].str.split(".", expand=True).loc[:, 0]
    df_file_dict["id"] = df_file_dict['filename'].str.split(
        sep, expand=True).loc[:, 1]
    df_file_dict["__uid"] = df_file_dict['filename'].str.split(
        sep, expand=True).loc[:, 0] + '_' + df_file_dict['filename'].str.split(sep, expand=True).loc[:, 1]

    # get overlapping source from one cohort
    file_key_base = df_file_dict["file_key"].value_counts(
        ascending=True).index[0]
    NSBJ = df_file_dict[df_file_dict["file_key"]
                        == file_key_base].loc[:, "__uid"].nunique()

    # filter filenames to include in source dict
    files_include = [file for source in source_dict.keys(
    ) for file in source_dict[source].keys() if source_dict[source][file]['include']]
    df_file_dict = df_file_dict[df_file_dict['file_key'].isin(files_include)]

    if stratify_by is None:
        stratify_by_list = []
    else:
        stratify_by = list(stratify_by)
        stratify_by_list = [
            var for var in stratify_by if 'factor' in variable_dict[var].keys()]
        print("--- Stratify sampling by :" + str(stratify_by_list))

    if len(stratify_by_list) == 0:
        if nsbj is not None:
            frac = min(int(nsbj), int(NSBJ)) / NSBJ
        uid_sampled = list(
            df_file_dict[df_file_dict["file_key"] == file_key_base].loc[:, "__uid"].sample(frac=frac))
        df_sample_info = df_file_dict[df_file_dict["__uid"].isin(uid_sampled)]
    else:
        grouping_df = None
        colnames_dict = []
        stratify_by_list = stratify_by_list+['__uid']
        for var in stratify_by_list:
            colnames_dict = colnames_dict + variable_dict[var]['src_names']
        for source_key in source_dict.keys():
            for file_key in source_dict[source_key].keys():
                fullname = source_dict[source_key][file_key]['path']
                colnames_df = pd.read_csv(
                    str(fullname), index_col=0, nrows=0).columns.tolist()
                usecols = list(
                    set(colnames_df).intersection(set(colnames_dict)))
                if len(usecols) > 0:
                    df = pd.read_csv(
                        str(fullname), low_memory=False, usecols=usecols)
                    df = fix_df_raw(variable_dict, df, source_key)
                    df = df.drop_duplicates()
                    if grouping_df is None:
                        grouping_df = df
                    else:
                        keys = list(set(df.columns).intersection(
                            set(grouping_df.columns)))
                        grouping_df = pd.merge(
                            left=grouping_df, right=df, on=keys, how='outer', copy=False)

        if nsbj is not None:
            frac = min(int(nsbj), int(NSBJ)) / NSBJ

        G = list(
            grouping_df.columns[~grouping_df.columns.isin(['__uid', '__anchor'])])
        uid_sampled = list(grouping_df.groupby(G)['__uid'].apply(
            lambda x: x.sample(frac=frac)).reset_index(drop=True))
        df_sample_info = df_file_dict[df_file_dict["__uid"].isin(
            list(uid_sampled))]

        print("Sucess!  " + str(uid_sampled)+" out of " +
              str(NSBJ) + " subjects are sampled!")
    return df_sample_info


def make_sbjs_ts(df_sample_info, source_dict, variable_dict, time_resolution, viz=False):

    df_sbjs_ts = pd.DataFrame()

    for source_key in list(df_sample_info['source_key'].unique()):

        # dataframe to store merged data for current source (if there are multiple sources)
        df_src_merged = None

        for file_key in list(df_sample_info['file_key'].unique()):

            # get stacked raw df (cohort-wise)
            df_raw = get_df_raw_from_csv(
                variable_dict, df_sample_info, source_key, file_key, viz=viz)

            # fix current raw file (cohort-wise)
            df_fix = fix_df_raw(variable_dict, df_raw, source_key)

            # aggregate by time resolution (cohort-wise)
            df_agg = agg_df_fix(variable_dict, df_fix, time_resolution)

            # append file key to variable names
            suf_vars = [var for var in variable_dict.keys() if var not in [
                '__uid', '__time', '__anchor']]
            df_agg_org = df_agg[list(set(df_agg.columns)-set(suf_vars))]
            df_agg_suf = df_agg[list(set(df_agg.columns).intersection(
                set(suf_vars)))].add_suffix('___'+str(file_key))
            df_agg = pd.concat([df_agg_org, df_agg_suf], axis=1)
            # merge multiple files
            if df_src_merged is None:  # first df_agg from current source
                df_src_merged = df_agg
                continue
            else:
                if '__time_bin' in df_agg.columns:
                    df_src_merged = pd.merge(left=df_src_merged, right=df_agg,
                                             left_on=['__uid', '__time_bin'], right_on=['__uid', '__time_bin'], how='outer',
                                             suffixes=('', '___right'),
                                             copy=False)
                else:
                    df_src_merged = pd.merge(left=df_src_merged, right=df_agg,
                                             left_on=['__uid'], right_on=['__uid'], how='left',
                                             suffixes=('', '___right'),
                                             copy=False)

                df_src_merged = df_src_merged.drop(
                    columns=df_src_merged.columns[df_src_merged.columns.str.endswith("___right")].to_list())

        df_sbjs_ts = pd.concat([df_sbjs_ts, df_src_merged], sort=False)

    return df_sbjs_ts


def make_episodes_ts(df_sbjs_ts, variable_dict, input_time_len, output_time_len, time_resolution, time_lag, anchor_gap):
    """ Summary: make a data frame of stacked episode time sequences

    Arges:

    Returns:

    Raises:

    """

    # factor type anchor
    if 'factor' in variable_dict['__anchor'].keys():
        for order in variable_dict['__anchor']['factor']['levels'].keys():
            if order == '1':
                df_sbjs_ts['__anchor'] = df_sbjs_ts['__anchor___1']
            if '__anchor___'+order in df_sbjs_ts.columns:
                df_sbjs_ts.loc[df_sbjs_ts['__anchor___'+order]
                               == 1, ['__anchor']] = int(order)
            else:
                print("--- No anchor order " + str(order) +
                      " found in sampled cohort")

    df_sbjs_ts = df_sbjs_ts.drop(
        columns=df_sbjs_ts.columns[df_sbjs_ts.columns.str.startswith("__anchor___")].to_list())

    # data frame to keep all episodes chunks from the same subject
    df_episodes_ts = pd.DataFrame()
    for uid in list(set(df_sbjs_ts['__uid'])):

        # get one sbject's dataframe
        df_sbj_ts = df_sbjs_ts[df_sbjs_ts['__uid'] == uid].copy()
        df_sbj_ts = df_sbj_ts.reset_index(drop=True)
        df_sbj_ts = df_sbj_ts.sort_values(by='__time_bin', ascending=True)

        # imputation for this subject
        for var in df_sbj_ts.columns[~df_sbj_ts.columns.isin(['__uid', '__anchor', '__time_bin'])]:
            var_dict = var.split('___')[0]
            if variable_dict[var_dict]['unique_per_sbj']:
                df_sbj_ts[var] = df_sbj_ts.loc[df_sbj_ts[var].first_valid_index(), var]

        # locate anchors
        df_sbj_output_times = df_sbj_ts.loc[df_sbj_ts.__anchor.notna(
        ), ['__anchor', '__time_bin']].reset_index(drop=True)

        # fix anchors by anchor_gap
        df_sbj_output_times = df_sbj_output_times[np.array(df_sbj_output_times.__time_bin.diff(1).isna()) | np.array(
            df_sbj_output_times.__time_bin.diff(1) >= anchor_gap//time_resolution)].reset_index(drop=True)

        for idx in list(df_sbj_output_times.index):

            sbj_y_start_time = df_sbj_output_times.loc[idx, '__time_bin'] - (
                input_time_len+time_lag)//time_resolution
            sbj_y_stop_time = df_sbj_output_times.loc[idx,
                                                      '__time_bin'] + output_time_len//time_resolution
            ts = pd.DataFrame(range(int(sbj_y_start_time), int(
                sbj_y_stop_time)), columns=['__time_bin'])

            df_sbj_episode_ts = pd.merge(
                left=ts, right=df_sbj_ts, left_on='__time_bin', right_on='__time_bin', how='left', copy=False)
            df_sbj_episode_ts['__uid'] = uid
            rel_start = int(-(input_time_len+time_lag)//time_resolution)
            rel_stop = rel_start + df_sbj_episode_ts.shape[0]
            df_sbj_episode_ts['episode_relative_time'] = list(
                range(rel_start, rel_stop))  # 0 included
            df_sbj_episode_ts['episode_relative_time'] = df_sbj_episode_ts['episode_relative_time'] * time_resolution
            df_sbj_episode_ts['episode_order'] = idx + 1
            df_sbj_episode_ts['__anchor'] = df_sbj_output_times.loc[idx, '__anchor']

            for var in df_sbj_episode_ts.columns.to_list():
                var_dict = var.split('___')[0]
                try:
                    # fulfill dummy factor or numeric outcomes
                    if variable_dict[var_dict]['output']:
                        df_sbj_episode_ts[var] = df_sbj_episode_ts.loc[df_sbj_episode_ts[var].first_valid_index(
                        ), var]
                except:
                    pass
                try:
                    if variable_dict[var_dict]['unique_per_sbj']:
                        df_sbj_episode_ts[var] = df_sbj_episode_ts.loc[df_sbj_episode_ts[var].first_valid_index(
                        ), var]
                except:
                    pass
                try:
                    f_bins = variable_dict[var_dict]['attr']['impute_per_sbj']['forward']//time_resolution
                    b_bins = variable_dict[var_dict]['attr']['impute_per_sbj']['backward']//time_resolution
                    if f_bins > 0:
                        df_sbj_episode_ts[var] = df_sbj_episode_ts[var].fillna(
                            method='ffill', limit=f_bins)
                    if b_bins > 0:
                        df_sbj_episode_ts[var] = df_sbj_episode_ts[var].fillna(
                            method='bfill', limit=b_bins)
                except:
                    pass

            df_episodes_ts = pd.concat(
                [df_episodes_ts, df_sbj_episode_ts], sort=False)
            df_episodes_ts = df_episodes_ts.drop(
                columns=df_episodes_ts.columns[df_episodes_ts.columns.str.startswith("__anchor___")].to_list())
            if 'factor' in variable_dict['__anchor'].keys():
                df_episodes_ts = df_episodes_ts.astype({'__anchor': 'int'})
            else:
                df_episodes_ts = df_episodes_ts.astype({'__anchor': 'float'})

    # print(df_episodes_ts.describe())
    return df_episodes_ts


def make_mvts_df_from_csv_pool(csv_pool_dir, nsbj, frac, source_dict, variable_dict, input_time_len, output_time_len, time_resolution, time_lag, anchor_gap, stratify_by=None, itered=False, viz=False, viz_ts=False):

    df_sample_info = make_sample_info_from_csv(
        csv_pool_dir=csv_pool_dir, source_dict=source_dict, variable_dict=variable_dict, nsbj=nsbj, frac=frac, stratify_by=stratify_by)
    df_sbjs_ts = make_sbjs_ts(df_sample_info, source_dict, variable_dict,
                              time_resolution, viz=viz)  # patient subset dataframe table
    if 'factor' in variable_dict['__anchor'].keys():
        if '__anchor___1' not in df_sbjs_ts.columns:
            if itered:
                return 'Warning: anchor must have at least 1 level.'
            itered = True
            print("--- System is resampling and will exit after 1 iteration.")
            make_mvts_df_from_csv_pool(csv_pool_dir, nsbj, frac, source_dict, variable_dict, input_time_len, output_time_len,
                                       time_resolution, time_lag, anchor_gap, stratify_by=stratify_by, itered=itered, viz=viz, viz_ts=viz_ts)

    if viz:
        fig_title = "Visualize Cleaned DataFrame"
        viz_df_hist(df_sbjs_ts, fig_title)

    df_episodes_ts = make_episodes_ts(
        df_sbjs_ts, variable_dict, input_time_len, output_time_len, time_resolution, time_lag, anchor_gap)

    if viz:
        fig_title = "Visualize Episode DataFrame"
        viz_df_hist(df_episodes_ts, fig_title)
    if viz_ts:
        fig_title = "Visualize Episode Data Variables over Time"
        viz_episode_ts(df_episodes_ts, fig_title)
    return df_episodes_ts


def cohort_fillna(train_df, valid_df, vars, method=None, fill_value=-333):

    if method == "mice":  # MICE(IterativeImputer)
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

    train_df[vars] = imputer.fit_transform(train_df[vars])
    valid_df[vars] = imputer.transform(valid_df[vars])

    train_df_imputed = train_df.copy()
    valid_df_imputed = valid_df.copy()

    return train_df_imputed, valid_df_imputed
