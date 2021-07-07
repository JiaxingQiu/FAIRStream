
import json

def load_source_dict(dict_folder_path):

    source_dict = None
    try:
        f = open(str(dict_folder_path)+'/source_dict.json', "r")
        source_dict = json.loads(f.read())
    except:
        print('Source dictionary not exist or not valid, please use querier.update_source_dict()')
    finally:
        return source_dict
    
def load_variable_dict(dict_folder_path):
    
    variable_dict = None
    try:
        f = open(str(dict_folder_path)+'/variable_dict.json', "r")
        variable_dict = json.loads(f.read())
    except:
        print("Variable dictionary not exist or not valid, please use querier.update_variable_dict()")
    finally:
        return variable_dict