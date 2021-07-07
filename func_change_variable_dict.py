import numpy
from func_load_dicts import load_variable_dict

def change_variable_dict(dict_folder_path):
    # read old variable dict
    variable_dict_old = load_variable_dict(dict_folder_path)

    # magic change happens

    variable_dict_new = {
        
        # id column in old sources / files
        "uid":{ 
            "source_names":{
                1:"id",
                2:"ID",
                3:"subject_id",
                4:"subject_id"
            }, # list of different source_names with its source id
            "label": "unique subject id for current study", # readable label of a variable
            "attr": {
                "type": "key", # type of a variable ("key" / "outcome" / "factor" / "numeric")
                "dtype": str(numpy.str_), # Built-in Python types : https://numpy.org/doc/stable/reference/arrays.dtypes.html
                "nlevel_min": 1, # min number of levels for factor variables
                "nlevel_max": None, # max number of levels
                "unique_per_sbj": True # whether or not a factor should be unique per row
            }
        },
        # time sequence index 
        "time":{
            "source_names":{
                1:"tsa",
                2:"tsa",
                3:"timeMinutes",
                4:"timeMinutes"
            },
            "label": "time since admission",
            "attr":{
                "type": "key",
                "dtype": str(numpy.int_),
                "value_min": 0, # min value boundary for numeric variables
                "value_max": None, # max value boundary for numeric variables
                "unit": "minute"
            }
        },
        
        "y":{
            "source_names":{
                2:"True_positive",
                4:"True positive"
            },
            "label": "time since admission",
            "attr":{
                "type": "outcome",
                "dtype": str(numpy.str_),
                "nlevel_min": 2, # min value boundary for numeric variables
                "nlevel_max": None, # max value boundary for numeric variables
                "unit": "minute"
            }
        },

        # subject age
        "age":{
            "source_names":{
                1:"age",
                3:"AGE"
            },
            "label": "subject age",
            "attr":{
                "type": "numeric",
                "dtype": str(numpy.int_),
                "value_min": 0,
                "value_max": 110,
                "unit": "year",
                "include": True
            }
        },
        # subject gender
        "gender":{
            "source_names":{
                1:"Sex",
                3:"Sex"
            },
            "label": "subject gender",
            "attr": {
                "type": "factor",
                "dtype": str(numpy.str_),
                "nlevel_min": 0,
                "nlevel_max": 10, 
                "unique_per_sbj": True,
                "include": True
            }
        },
        # subject race
        "race":{
            "source_names":{
                1:"Race",
                3:"RACE"
            },
            "label": "subject race",
            "attr": {
                "type": "factor",
                "dtype": str(numpy.str_),
                "nlevel_min": 0,
                "nlevel_max": 20, 
                "unique_per_sbj": True,
                "include": True
            }
        },
        # subject ethnicity
        "ethnicity":{
            "source_names":{
                0:"ethnicity",
                0:"Ethnicity"
            },
            "label": "subject ethnicity",
            "attr": {
                "type": "factor",
                "dtype": str(numpy.str_),
                "nlevel_min": 0,
                "nlevel_max": 10, 
                "unique_per_sbj": True,
                "include": True
            }
        },
        "temperature":{
            "source_names":{
                1:"Temp",
                3:"tempc"
            },
            "label": "subject body temperature",
            "attr":{
                "type": "numeric",
                "dtype": str(numpy.float_),
                "value_min": 5,
                "value_max": 60,
                "unit": "celsius",
                "include": True
            }
        },
        "heart_rate":{
            "source_names":{
                1:"hr",
                3:"heartrate"
            },
            "label": "subject heart rate",
            "attr":{
                "type": "numeric",
                "dtype": str(numpy.int_),
                "value_min": 10,
                "value_max": 200,
                "unit": "beats per minute",
                "include": True
            }
        },
        "systolic_blood_pressure":{
            "source_names":{
                1:"SBP",
                3:"sysbp"
            },
            "label": "subject systolic blood pressure",
            "attr":{
                "type": "numeric",
                "dtype": str(numpy.float_),
                "value_min": 0,
                "value_max": 100,
                "unit": "mm Hg",
                "include": True
            }
        },
        "diastolic_blood_pressure":{
            "source_names":{
                1:"DBP",
                3:"diasbp"
            },
            "label": "subject diastolic blood pressure",
            "attr":{
                "type": "numeric",
                "dtype": str(numpy.float_),
                "value_min": 0,
                "value_max": 100,
                "unit": "mm Hg",
                "include": True
            }
        },
        "resp_rate":{
            "source_names":{
                1:"rr",
                3:"resprate"
            },
            "label": "subject diastolic blood pressure",
            "attr":{
                "type": "numeric",
                "dtype": str(numpy.float_),
                "value_min": 0,
                "value_max": 200,
                "unit": "mm Hg",
                "include": True
            }
        }
    }

    return variable_dict_new