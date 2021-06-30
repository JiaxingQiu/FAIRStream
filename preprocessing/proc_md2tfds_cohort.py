import pandas as pd
import proc_merged_sbj_df
import proc_control_data_quality
import proc_design_event_seq
import proc_convert_tfds

def proc_md2tfds_cohort(id_list, vars_include, source_dict, variable_dict, time_bin, time_unit_before, time_unit_after):

    for sbj_id in id_list:
        
        sbj_df = proc_merged_sbj_df(sbj_id, vars_include, source_dict, variable_dict, time_bin) # patient subset dataframe table
        sbj_df = proc_control_data_quality(sbj_df, variable_dict)
        sbj_events = proc_design_event_seq(sbj_df, time_unit_before, time_unit_after)
        cohort_event_seq = pd.concat([cohort_event_seq, sbj_events])

    dataset = proc_convert_tfds(cohort_event_seq, time_unit_before, time_unit_after)




    return dataset