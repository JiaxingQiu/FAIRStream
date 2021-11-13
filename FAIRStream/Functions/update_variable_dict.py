def update_variable_dict():
    
    variable_dict = {
        # id column in old sources / files
        "__uid": {
            "src_names": [
                "id",
                "ID",
                "subject_id",
                "subject_id"
            ],  # list of different names with its source id
            "label": "unique subject id for current study",  # readable label of a variable
            "unique_per_sbj": True,
        },
        # time sequence index
        "__time": {
            "src_names": [
                "tsa",
                "tsa",
                "timeMinutes",
                "timeMinutes"
            ],
            "label": "time since admission",
            "unit": "minute"
        },
        "__anchor": {
            "src_names": [
                "True_positive",
                "True positive"
            ],
            "label": "anchor for an episode",
            "unique_per_sbj": False,
            "factor": {
                "levels": {
                    "__nbc": ["nan"], # whether or not include "__non" (no blood culture) as one of anchor option
                    "__neg": ["0", "0.0"], # negative culture # if neg is higher than non
                    "__pos": ["1", "1.0"] # positive culture
                },
                "impute_per_sbj":{
                    "nan_level": "__nbc" # create a seperate column for nan indicator
                }
            }
        },

        "y": {
            "output": True,
            "src_names": [
                "True_positive",
                "True positive"
            ],
            "label": "Event outcome result",
            "unique_per_sbj": False,
            "factor": {
                "levels": { # ordinal
                    "nbc": ["nan"], # whether or not include "__non" (no blood culture) as one of anchor option
                    "neg": ["0", "0.0"], # negative test
                    "pos": ["1", "1.0"] # positive test
                },
                "impute_per_sbj":{
                    "nan_level": "nbc"
                }
            }
        },
        # subject age
        "age": {
            "input": True,
            "src_names": [
                "age",
                "AGE"
            ],
            "label": "age at admission",
            "unique_per_sbj": True,
            "numeric": {
                "scaler": "none",
                
                "unit": "year",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 110,
                },
                "impute_per_sbj": {
                    "forward": 0,
                    "backward": 0
                }
            }
        },
        # subject gender
        "gender": {
            "input": False,
            "src_names": [
                "Sex",
                "Sex"
            ],
            "label": "subject gender",
            "unique_per_sbj": True,
            "factor": {
                "levels": {
                    "Male": ["male", "Male", "0"],
                    "Female": ["female", "Female", "1"]
                },
                "impute_per_sbj":{
                    
                    "nan_level": "unknown"
                }
            }
        },
        # subject race
        "race": {
            "input": False,
            "src_names": [
                "Race",
                "RACE"
            ],
            "label": "subject race",
            "unique_per_sbj": True,
            "factor": {
                "levels": {
                    "Black": 1,
                    "White": 2
                },
                "impute_per_sbj":{
                    
                    "nan_level": "White"
                }
            }
        },
        # subject ethnicity
        "ethnicity": {
            "input": False,
            "src_names": [
                "ethnicity",
                "Ethnicity"
            ],
            "label": "subject ethnicity",
            "unique_per_sbj": True,
            "factor": {
                "levels": {
                    "African American": ["aa", "African american"],
                    "Asian": ["asian", "Asian"],
                    "Histopian": ["hist", "histopian", "Histopian"]
                },
                "impute_per_sbj":{
                    
                    "nan_level": "White"
                }
            }
        },
        "temp": {
            "input": True,
            "src_names": [
                "Temp",
                "tempc"
            ],
            "label": "subject body temperature",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "minmax",
                "unit": "celsius",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 5,
                    "value_max": 60,
                },
                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }

            }
        },
        "heart_rate": {
            "input": True,
            "src_names": [
                "hr",
                "heartrate"
            ],
            "label": "subject heart rate",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                
                "unit": "beats per minute",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 10,
                    "value_max": 200
                },
                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "systolic_blood_pressure": {
            "input": True,
            "src_names": [
                "SBP",
                "sysbp"
            ],
            "label": "subject systolic blood pressure",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                
                "unit": "mm Hg",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 100
                },
                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "diastolic_blood_pressure": {
            "input": True,
            "src_names": [
                "DBP",
                "diasbp"
            ],
            "label": "subject diastolic blood pressure",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                
                "unit": "mm Hg",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 100
                },
                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "resp_rate": {
            "input": True,
            "src_names": [
                "rr",
                "resprate"
            ],
            "label": "subject respiratory rate",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 200
                },
                "unit": "mm Hg",
                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "spo2": {
            "input": False,
            "src_names": [
            ],
            "label": "SpO2",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 79
                },
                "unit": "TODO",
                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "glucose": {
            "input": True,
            "src_names": ['GLUCOSE', 'Glucose'],
            "label": "Glucose",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 49,
                    "value_max": 460
                },
                "unit": "TODO",
                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "bilirubin": {
            "input": True,
            "src_names": ['TOTAL.BILIRUBIN', 'bilirubin'],
            "label": "Bilirubin",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 50
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "potassium": {
            "input": True,
            "src_names": ['POTASSIUM', 'Potassium'],
            "label": "Potassium",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 2.4,
                    "value_max": 6.6
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "albumin": {
            "input": True,
            "src_names": ['Albumin', 'ALBUMIN'],
            "label": "Albumin",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 5
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "calcium": {
            "input": True,
            "src_names": ['CALCIUM', 'Calcium'],
            "label": "Calcium",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 6.1,
                    "value_max": 12
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "wbc": {
            "input": True,
            "src_names": ['WHITE.BLOOD.CELL.COUNT', 'WBC'],
            "label": "WBC",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 33.85
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        # "pt": {
        #     "input":False,
        #     "src_names": [ ,
        #     ],
        #     "label": "PT",
        #     "unique_per_sbj": False,
        #     "attr": {
        #         "numeric":{
        #
        #         "cutoff":{"quantile_min": 0.0001,
        #            "quantile_max": 0.9999,"value_min": 0,
        #         "value_max": 5,
        #         "unit": "TODO",
        #
        #         "impute_per_sbj": {
        #             "forward": 24*60,
        #             "backward": 12*60
        #         }
        #     }
        # },
        "creatinine": {
            "input": True,
            "src_names": ['CREATININE', 'Creatinine'],
            "label": "Creatinine",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 10
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
                
            }
        },
        "platelet_count": {
            "input": True,
            "src_names": ['PLATELET.COUNT', 'plateletcount'],
            "label": "PlateletCount",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 1001
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "alt": {
            "input": True,
            "src_names": ['ALT.GPT', 'ALT'],
            "label": "ALT",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 1085
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "alp": {
            "input": True,
            "src_names": ['ALKALINE.PHOSPHATASE', 'ALP'],
            "label": "ALP",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 800
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "ast": {
            "input": True,
            "src_names": ['AST.GOT', 'AST'],
            "label": "AST",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 1203
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "paco2": {
            "input": True,
            "src_names": ['PCO2', 'PaCO2'], # arterial
            "label": "PaCO2",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 100.5
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "chloride": {
            "input": True,
            "src_names": ['CHLORIDE', 'Chloride'],
            "label": "Chloride",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 83,
                    "value_max": 132
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "troponin": {
            "input": True,
            "src_names": ['TROPONIN.I', 'Troponin'],
            "label": "Troponin",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 23.5
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "ptt": {
            "input": True,
            "src_names": ['PARTIAL.THROMBOPLASTIN.TIME', 'PTT'],
            "label": "partial_thromboplastin_time",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                

                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 140
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "lactate": {
            "input": True,
            "src_names": ['Lactate', 'LACTIC.ACID'],
            "label": "Lactate",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 19.1
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "bun": {
            "input": True,
            "src_names": ['BLOOD.UREA.NITROGEN', 'BUN'],
            "label": "BUN",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 143
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        },
        "magnesium": {
            "input": True, 
            "src_names": ['MAGNESIUM', 'Magnesium'],
            "label": "Magnesium",
            "unique_per_sbj": False,
            "numeric": {
                "scaler": "none",
                "cutoff": {
                    "quantile_min": 0.0001,
                    "quantile_max": 0.9999,
                    "value_min": 0,
                    "value_max": 3.4
                },
                "unit": "TODO",

                "impute_per_sbj": {
                    "forward": 24*60,
                    "backward": 12*60
                }
            }
        }
    }

    return variable_dict
