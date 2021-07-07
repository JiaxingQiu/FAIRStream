""" MediWorker class. 

Module description details
    
    MediWorker is the parent class (initial role) for all the subclass players in FAIRstream workflow --
    Querier Engineer Learner Reporter -- to inherit. 
    
    All workers know (properties)
        dict_folder_path: where the dictionaries (cookbook) for the study
    
    All workers can (functions)
        load_source_dict: read source file dictionary
        load_variable_dict: read variables dictionary


    Usage example:

"""
import os
from func_load_dicts import load_source_dict, load_variable_dict

class MediWorker:
    
    def __init__(self, wd):
        # set study working directory
        self.wd = wd
        # set dictionary folder under current working direction
        self.dict_folder_path = str(self.wd) + '/dictionary'
        if not os.path.exists(self.dict_folder_path):
            os.mkdir(self.dict_folder_path)

    def __str__(self):
        return '\n'.join([
            f'Working directory: {self.wd}',
            f'Study dictionary path: {self.dict_folder_path}'
            ])
    

    def load_source_dict(self):
        self.source_dict = load_source_dict(self.dict_folder_path)
        

    def load_variable_dict(self): 
        self.variable_dict = load_variable_dict(self.dict_folder_path)
        
    