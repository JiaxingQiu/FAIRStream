def update_csv_source_dict():
    # note: file keys list must be the same across sources
    raw_data_dir = '/Users/jiaxingqiu/Documents/PreVent/Analysis/data/hourly/'
    # csv_source_dict = { 
    #     "PreVent": {
    #         "SPO2_pct_stats": {
    #             "include": True,
    #             "path": raw_data_dir + "SPO2_pct_hourly_statistics_bap_v2_0_deidentified.csv",
    #             "label": "",
                
    #         },
    #         "HR_stats": {
    #             "include": True,
    #             "path": raw_data_dir + "HR_hourly_statistics_bap_v2_0_deidentified.csv",
    #             "label": "",
                
    #         },
    #         "PB_BI": {
    #             "include": True,
    #             "path": raw_data_dir + "PeriodicBreathing_v2_agg_hourly_deidentified.csv",
    #             "label": "",
                
    #         },
    #         "MaxCrossCorrHR_SPO2_BI": {
    #             "include": True,
    #             "path": raw_data_dir + "MaxCrossCorrHR_SPO2_pct_v1_agg_hourly_deidentified.csv",
    #             "label": "",
                
    #         },
    #         "Brady_100_BI": {
    #             "include": True,
    #             "path": raw_data_dir + "Brady_100_v2_agg_hourly_deidentified.csv",
    #             "label": "",
                
    #         },
    #         "Desat_80_BI": {
    #             "include": True,
    #             "path": raw_data_dir + "Desat_80_v2_agg_hourly_deidentified.csv",
    #             "label": "",
                
    #         },
    #         "PrimaryOutcome": {
    #             "include": True,
    #             "path": raw_data_dir + "40w_primary_outcome.csv",
    #             "label": "",
                
    #         },
    #         "Demo_base": {
    #             "include": True,
    #             "path": raw_data_dir + "base_cleaned.csv",
    #             "label": "",
                
    #         },
    #         "Cross_corr_HR_SPO2":{
    #             "include": True,
    #             "path": raw_data_dir + "MaxCrossCorrHR_SPO2_pct_10mins_values_bap_v2_0_deidentified.csv",
    #             "label": ""
    #         }
    #     }
    # }
    print(raw_data_dir)
    #return csv_source_dict
