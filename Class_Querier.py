""" Querier class. One of the workers in FAIRStream workflow, do the querying tasks and make / change study dictionaries for all workers

Module description details
    
    Querier is one player in FAIRstream workflow, inherited from MediWorker class. 
    
    Querier has access to mulitple sources involved in one study, 
    a typical data source could be querying request commans to a database, 
    or a location for csv files in someone' drive.

    
    Querier properties:
        dict_folder_path: where the dictionaries (cookbook) for the study
    
    Querier functions:
        update_source_dict: read source file dictionary
        update_variable_dict: read variables dictionary
    
    Usage example:

"""
import json

from Class_MediWorker import MediWorker
from func_change_source_dict import change_source_dict
from func_change_variable_dict import change_variable_dict


class Querier(MediWorker):
    
    def __init__(self, wd):
        MediWorker.__init__(self, wd)

    
    def __str__(self):
        return '\n'.join([
            f'Querier can load and update study dictionaries! ',
            f'directories location: {self.dict_folder_path}'
            ])

    
    
    # UI / UX tool that ask user to input study source file dictionary
    def update_source_dict(self):
        self.source_dict_new = change_source_dict(self.dict_folder_path)
        with open(self.dict_folder_path + '/source_dict.json', 'w') as f:
            json.dump(self.source_dict_new, f)
        print('Success: Querier has updated source dictionary!')

    # UI / UX tool that ask user to input study vairable dictionary
    def update_variable_dict(self):
        self.variable_dict_new = change_variable_dict(self.dict_folder_path)
        with open(self.dict_folder_path + '/variable_dict.json', 'w') as f:
            json.dump(self.variable_dict_new, f)
        print('Success: Querier has updated variable dictionary!')

    def load_source_dict(self):
        super().load_source_dict()

    def load_variable_dict(self):
        super().load_variable_dict()
        
        
test= 'minute'
'\n'.join([
    f'An event for the study is defined as following : ',
    f'    Time {str(11)}  {test}  before an event outcome',
    f'    Time {str(12)}  {test}  after an event outcome'
])