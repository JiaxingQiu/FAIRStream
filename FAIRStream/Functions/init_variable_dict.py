def init_variable_dict():
    variable_dict_demo = {
        "__uid": {
            "src_names": ["id", "subjectnbr", "ID"],
            "label": "unique study subject id",
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
            "label": "anchor of an episode",
            "unique_per_sbj": False,
            "factor": {
                "levels": {
                    "__1": ["1", "1.0"],
                    "__2": ["2", "2.0"],
                    "__3": ["3", "3.0"]
                }
            }
        },
        "log_BI": {
            "output": True,  # set output to True if this variable is an output
            "src_names": ["log_burden_index"],
            "label": "log of episode burden index",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                
                "unit": "log(percentage of daily episode duration +0.0001)",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": -8,
                    "value_max": 0,
                },
                "impute_per_sbj": {
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        "age": {
            "input": False,  # set input to True if this variable is an input
            "src_names": ["Age"],
            "label": "patient age at admission",
            "unique_per_sbj": True,
            "numeric": {
                "scaler": "none",
                 # "minmax", "standard", "maxabs", "robust", "rank", "power"
                "unit": "year",
                "cutoff": {  # cohort
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 120,
                },
                "impute_per_sbj": {
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        "HRMean": {
            "input": False,
            "src_names": ["HRMean", "HeartRate"],
            "label": "patient houly mean heart rate",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                
                "unit": "beats per minute",
                "cutoff": {  # cohort
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 40,
                    "value_max": 140,
                },
                "impute_per_sbj": {
                    "forward": 1,
                    "backward": 0
                }
            }
        }
    }
    return variable_dict_demo
