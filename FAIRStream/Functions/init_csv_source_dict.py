def init_csv_source_dict():
    csv_source_dict_demo =  {
        "source_1": {
            "csv_file_1": {
                "include": True,
                "path": "cohort_1 csv_file_1 full path here",
                "info": "a short description of cohort_1 csv_file_1",
                
            },
            "file_2": {
                "include": True,
                "path": "cohort_1 csv_file_2 full path here",
                "info": "a short description of cohort_1 csv_file_2",
                
            }
        },
        "source_2": { 
            "csv_file_1": {
                "include": True,
                "path": "cohort_2 csv_file_1 full path here",
                "info": "a short description of cohort_1 csv_file_1",
                
            },
            "file_2": {
                "include": False,
                "path": "cohort_2 csv_file_2 full path here",
                "info": "a short description of cohort_1 csv_file_2",
                
            }
        }
    }
    return csv_source_dict_demo
