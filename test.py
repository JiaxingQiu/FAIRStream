import json
import os
from func_load_dicts import load_source_dict, load_variable_dict
import pandas as pd
import FAIRStream


bsi_stream = FAIRStream.FAIRStream('X:\Joy\BSI\FAIRStream')
bsi_stream.querier.update_variable_dict()
dict_folder_path = 'X:\Joy\BSI\FAIRStream\data\dictionary'
source_dict = load_source_dict(dict_folder_path)
print(source_dict.keys())
