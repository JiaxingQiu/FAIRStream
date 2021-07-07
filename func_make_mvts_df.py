import pandas as pd
from func_merge_sbj_df import merge_sbj_df
from func_seq_sbj_events import seq_sbj_events

def make_mvts_df(uid_list, source_dict, variable_dict, event):

    for uid in uid_list:

        sbj_df = merge_sbj_df(uid, source_dict, variable_dict, event.time_resolution) # patient subset dataframe table
        sbj_events = seq_sbj_events(sbj_df, event.time_before, event.time_after, event.time_gap)
        cohort_events_df = pd.concat([cohort_events_df, sbj_events])

    return cohort_events_df


def make_mvts_tfds(df, event):

    tfds = df
    return tfds
