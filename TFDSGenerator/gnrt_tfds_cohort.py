import pandas as pd
import gnrt_merged_sbj_df
import gnrt_clean_sbj_df
import gnrt_event_seq
import gnrt_convert_tfds

def gnrt_tfds_cohort(id_list, source_dict, variable_dict, time_binwidth, bins_before, bins_after):

    for sbj_id in id_list:
        
        sbj_df = gnrt_merged_sbj_df(sbj_id, source_dict, variable_dict, time_binwidth) # patient subset dataframe table
        sbj_df = gnrt_clean_sbj_df(sbj_df, variable_dict)
        sbj_events = gnrt_event_seq(sbj_df, bins_before, bins_after)
        cohort_event_seq = pd.concat([cohort_event_seq, sbj_events])

    dataset = gnrt_convert_tfds(cohort_event_seq, bins_before, bins_after)

    return dataset