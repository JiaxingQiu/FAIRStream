import numpy
from func_load_dicts import load_source_dict

def change_source_dict(dict_folder_path):
    source_dict_old = load_source_dict(dict_folder_path)

    data_path = dict_folder_path.replace('/dictionary','/data')
    source_dict_new = {
        "uva":{
            1:{
                "path": data_path + "/bsi_old_deidentified_final.csv",
                "info": "Vital signs data from UVA",
                "keys": { # key columns info
                    "id": { # id column info in this file
                        "colname": "id" 
                    },
                    "time": {# time-related column info in this file
                        "colname": "tsa",
                        "base_unit": "minute",
                        "dtype": str(numpy.int_)
                    } 
                },
                "include":True
            },
            2:{
                "path": data_path + "/uva_lab.csv",
                "info": "Lab results data from UVA",
                "keys": { # key columns info
                    "id": { # id column info in this file
                        "colname": "ID" 
                    },
                    "time": {# time-related column info in this file
                        "colname": "tsa",
                        "base_unit": "minute",
                        "dtype": str(numpy.int_)
                    } 
                },
                "include":True
            }
        },
        "mimic":{
            1:{
                "path": data_path + "/mimic_patient_data_minutes.csv",
                "info": "Vital signs data from MIMIC",
                "keys": { # key columns info
                    "id": { # id column info in this file
                        "colname": "subject_id" 
                    },
                    "time": {# time-related column info in this file
                        "colname": "timeMinutes",
                        "base_unit": "minute",
                        "dtype": str(numpy.int_)
                    } 
                },
                "include":True
            },
            2:{
                "path": data_path + "/mimic_labs_minutes_combined.csv",
                "info": "Lab results data from MIMIC",
                "keys": {  # key columns info
                    "id": { # id column info in this file
                        "colname": "subject_id" 
                    },
                    "time": {# time-related column info in this file
                        "colname": "timeMinutes",
                        "base_unit": "minute",
                        "dtype": str(numpy.int_)
                    } 
                },
                "include":True
            }
        }
    }
    return source_dict_new