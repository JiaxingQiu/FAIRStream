def init_csv_source_dict():
    csv_source_dict_demo = {
        "cohort_1": {
            "csv_file_1": {
                "input": True,
                "path": "cohort_1 csv_file_1 full path here",
                "label": "a short description of cohort_1 csv_file_1",
                
            },
            "file_2": {
                "input": True,
                "path": "cohort_1 csv_file_2 full path here",
                "label": "a short description of cohort_1 csv_file_2",
                
            }
        },
        "cohort_2": { 
            "input": True,
            "csv_file_1": {
                "path": "cohort_2 csv_file_1 full path here",
                "label": "a short description of cohort_1 csv_file_1",
                
            },
            "file_2": {
                "input": True,
                "path": "cohort_2 csv_file_2 full path here",
                "label": "a short description of cohort_1 csv_file_2",
                
            }
        }
    }
    return csv_source_dict_demo

def init_variable_dict():
    variable_dict_demo = {
        "__uid": {
            "src_names": ["id","subjectnbr"],  # list of different names with its source id
            "label": "unique study subject id",  # readable label of a variable
            "unique_per_sbj": True
        },
        "__time": {
            "src_names": ["hoursincebirth"],
            "label": "time since birth",
            "unique_per_sbj": False,
            "unit": "hour"
        },
        "__anchor": {
            "src_names": ["y"],
            "label": "primary outcome result",
            "unique_per_sbj": False,
            "factor": {
                "levels": {
                    "1": ["1","1.0"],
                    "2": ["2","2.0"],
                    "3": ["3","3.0"]
                }
            }
        },
        "BI": {
            "input": True,
            "src_names": ["burden_index"],
            "label": "episode burden index",
            "unique_per_sbj": False,
            "numeric": {
                "unit": "percentage of daily episode duration * 3600",
                "cutoff":{ #cohort
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": 0,
                    "value_max": 100000,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        }
    }
    return variable_dict_demo

def update_sql_source_dict():
    sql_source_dict = []
    return sql_source_dict

def update_csv_source_dict():
    # note: file keys list must be the same across sources
    raw_data_dir = '/Users/jiaxingqiu/Documents/PreVent/Analysis/data/hourly/'
    csv_source_dict = { 
        "PreVent": {
            "SPO2_pct_stats": {
                "include": True,
                "path": raw_data_dir + "SPO2_pct_hourly_statistics_bap_v2_0_deidentified.csv",
                "label": "",
                
            },
            "HR_stats": {
                "include": True,
                "path": raw_data_dir + "HR_hourly_statistics_bap_v2_0_deidentified.csv",
                "label": "",
                
            },
            "PB_BI": {
                "include": True,
                "path": raw_data_dir + "PeriodicBreathing_v2_agg_hourly_deidentified.csv",
                "label": "",
                
            },
            "MaxCrossCorrHR_SPO2_BI": {
                "include": False,
                "path": raw_data_dir + "MaxCrossCorrHR_SPO2_pct_v1_agg_hourly_deidentified.csv",
                "label": "",
                
            },
            "Brady_100_BI": {
                "include": False,
                "path": raw_data_dir + "Brady_100_v2_agg_hourly_deidentified.csv",
                "label": "",
                
            },
            "Desat_80_BI": {
                "include": False,
                "path": raw_data_dir + "Desat_80_v2_agg_hourly_deidentified.csv",
                "label": "",
                
            },
            "PrimaryOutcome": {
                "include": False,
                "path": raw_data_dir + "40w_primary_outcome.csv",
                "label": "",
                
            },
            "Demo_base": {
                "include": False,
                "path": raw_data_dir + "base_cleaned.csv",
                "label": "",
                
            }
        }
    }

    return csv_source_dict

def update_variable_dict():
    variable_dict = {
        "__uid": {
            "src_names": ["id","subjectnbr"],  # list of different names with its source id
            "label": "unique study subject id",  # readable label of a variable
            "unique_per_sbj": True
        },
        "__time": {
            "src_names": ["hoursincebirth"],
            "label": "time since birth",
            "unique_per_sbj": False,
            "unit": "hour"
        },
        # "__anchor": {
        #     "src_names": ["y"], # factor output only can have levels 1,2,3...
        #     "label": "primary outcome result",
        #     "unique_per_sbj": False,
        #     "factor": {
        #         "levels": {
        #             "1": ["1","1.0"],
        #             "2": ["2","2.0"],
        #             "3": ["3","3.0"]
        #         }
        #     }
        # },
        "__anchor": {
            "src_names": ["log_burden_index"],
            "label": "log of episode burden index",
            "unique_per_sbj": False,
            "numeric": {
                "unit": "log(percentage of daily episode duration +0.0001)",
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": -10000,
                    "value_max": 100000,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        "y": {
            "output":False,
            "src_names": ["log_BI"], # factor output only can have levels 1,2,3...
            "label": "primary outcome result",
            "unique_per_sbj": False,
            "factor": {
                "levels": {
                    "1": ["1","1.0"],
                    "2": ["2","2.0"],
                    "3": ["3","3.0"]
                }
            }
        },
        "BI": {
            "input": False,
            "src_names": ["burden_index"],
            "label": "episode burden index",
            "unique_per_sbj": False,
            "numeric": {
                "unit": "percentage of daily episode duration * 3600",
                "cutoff":{ #cohort
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": 0,
                    "value_max": 100000,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        "log_BI": {
            "output": True,
            "src_names": ["log_burden_index"],
            "label": "log of episode burden index",
            "unique_per_sbj": False,
            "numeric": {
                "unit": "log(percentage of daily episode duration +0.0001)",
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": -8,
                    "value_max": 0,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        
        "HRMean": {
            "input": True,
            "src_names": ["HourlyHRMean_v1"],
            "label": "hourly mean heart rate",
            "unique_per_sbj": False,
            "numeric": {
                "unit": "beats per minute",
                 "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": 0,
                    "value_max": 300,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        
        "HRStd": {
            "input": True,
            "src_names": ["HourlyHRStd_v1"],
            "label": "hourly standard deviation of heart rate",
            "unique_per_sbj": False,
            "numeric": {
                "unit": None,
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": -100,
                    "value_max": 100,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        
        "HRSkewness": {
            "input": True,
            "src_names": ["HourlyHRSkewness_v1"],
            "label": "hourly skewness of heart rate",
            "unique_per_sbj": False,
            "numeric": {
                "unit": None,
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": -100,
                    "value_max": 100,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },

        "HRKurtosis": {
            "input": True,
            "src_names": ["HourlyHRKurtosis_v1"],
            "label": "hourly skewness of heart rate",
            "unique_per_sbj": False,
            "numeric": {
                "unit": None,
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": -100,
                    "value_max": 100,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },

        "SPO2_pctMean": {
            "input": True,
            "src_names": ["HourlySPO2_pctMean_v1"],
            "label": "hourly mean SPO2 percentage",
            "unique_per_sbj": False,
            "numeric": {
                "unit": "beats per minute",
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": 0,
                    "value_max": 100,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        
        "SPO2_pctStd": {
            "input": True,
            "src_names": ["HourlySPO2_pctStd_v1"],
            "label": "hourly standard deviation of SPO2 percentage",
            "unique_per_sbj": False,
            "numeric": {
                "unit": None,
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": -100,
                    "value_max": 100,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        
        "SPO2_pctSkewness": {
            "input": True,
            "src_names": ["HourlySPO2_pctSkewness_v1"],
            "label": "hourly skewness of SPO2 percentage",
            "unique_per_sbj": False,
            "numeric": {
                "unit": None,
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": -100,
                    "value_max": 100,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },

        "SPO2_pctKurtosis": {
            "input": True,
            "src_names": ["HourlySPO2_pctKurtosis_v1"],
            "label": "hourly Kurtosis of heart rate",
            "unique_per_sbj": False,
            "numeric": {
                "unit": None,
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": -100,
                    "value_max": 100,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },

        "birth_weight": {
            "input": False,
            "src_names": ["baby_weight"],
            "label": "subject birth weight",
            "unique_per_sbj": True,
            "numeric": {
                "unit": "grams",
                "cutoff":{
                    "quantile_min": 0.0005,
                    "quantile_max": 0.9995,
                    "value_min": 300,
                    "value_max": 3000,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        "ga_weeks": {
            "input": False,
            "src_names": ["baby_gaweeks"],
            "label": "subject birth weight",
            "unique_per_sbj": True,
            "numeric": {
                "unit": "week",
                "cutoff":{
                    "quantile_min": None,
                    "quantile_max": None,
                    "value_min": None,
                    "value_max": None,
                },
                "impute_per_sbj":{
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        
        "gender": {
            "input": False,
            "src_names": ["baby_gender.factor"],
            "label": "subject gender",
            "unique_per_sbj": True,
            "factor": {
                "levels": {
                    "Male": ["male", "Male", "0"],
                    "Female": ["female", "Female", "1"]
                }
            }
        }
    }
    return variable_dict
