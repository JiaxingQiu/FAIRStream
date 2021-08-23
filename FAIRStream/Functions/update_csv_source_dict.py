def update_csv_source_dict():
    csv_source_dict={
        "uva": {
            "vital": {
                "include": True,
                "path": "/Users/jiaxingqiu/Documents/BSI/code/DeepDiag/data/bsi_old_deidentified_final.csv",
                "info": "Vital signs data from UVA"
            },
            "lab": {
                "include": True,
                "path": "/Users/jiaxingqiu/Documents/BSI/code/DeepDiag/data/uva_lab.csv",
                "info": "Lab results data from UVA"}
        },
        "mimic": {
            "vital": {
                "path": "/Users/jiaxingqiu/Documents/BSI/code/DeepDiag/data/mimic_patient_data_minutes.csv",
                "info": "Vital signs data from MIMIC", 
                "include": True
            },
            "lab": {
                "path": "/Users/jiaxingqiu/Documents/BSI/code/DeepDiag/data/mimic_labs_minutes_combined.csv",
                "info": "Lab results data from MIMIC", 
                "include": True
            }
        }
    }
    return csv_source_dict
