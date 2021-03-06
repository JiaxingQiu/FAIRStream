""" Querier class. One of the workers in FAIRStream workflow, do the querying tasks and make / change study dictionaries for all workers

Module description details
    
    Querier is one player in FAIRstream workflow, inherited from Goblin class. 
    
    Querier has access to mulitple sources involved in one study, 
    a typical data source could be querying request commans to a database, 
    or a location for csv files in someone' drive.

    
    Querier properties:
        meta_dir: where the dictionaries (cookbook) for the study
    
    Querier Functions:
        update_csv_source_dict: read source file dictionary
        update_variable_dict: read variables dictionary
    
    Usage example:
 
"""
import json

from Classes.Goblin import Goblin
from Functions.init_csv_source_dict import *
from Functions.init_variable_dict import *
from Functions.update_csv_source_dict import *
from Functions.update_sql_source_dict import *
from Functions.update_variable_dict import *
from Functions.cmp_src_csv import *
from Functions.create_csv_pool import *


class Querier(Goblin):
    
    def __init__(self, work_dir):
        Goblin.__init__(self, work_dir)
        self.init_csv_source_dict()
        self.init_variable_dict()
        self.read_csv_source_dict()
        self.read_variable_dict()
        
        
    def __str__(self):
        return '\n'.join([
            f'Querier can prepare meta data for your study! ',
            f'Meta data directory : {self.meta_dir}'
            ])
    
    def init_csv_source_dict(self):
        self.csv_source_dict_demo = init_csv_source_dict()
        with open(self.meta_dir + '/csv_source_dict_demo.json', 'w') as f:
            json.dump(self.csv_source_dict_demo, f)
        print('Success: Querier has initiated a csv source dictionary in:' + str(self.meta_dir) + '/csv_source_dict_demo.json')
    
    def init_variable_dict(self):
        self.variable_dict_demo = init_variable_dict()
        with open(self.meta_dir + '/variable_dict_demo.json', 'w') as f:
            json.dump(self.variable_dict_demo, f)
        print('Success: Querier has initiated a variable dictionary in:' + str(self.meta_dir) + '/variable_dict_demo.json')
    
    
    def update_csv_source_dict(self): # UI / UX tool that ask user to input study source file dictionary
        self.csv_source_dict_new = update_csv_source_dict()
        with open(self.meta_dir + '/csv_source_dict.json', 'w') as f:
            json.dump(self.csv_source_dict_new, f)
        print('Success: Querier has updated csv source dictionary!')
    
    def update_sql_source_dict(self):
        self.sql_source_dict_new = update_sql_source_dict()
        with open(self.meta_dir + '/sql_source_dict.json', 'w') as f:
            json.dump(self.sql_source_dict_new, f)
        print('Success: Querier has updated sql source dictionary!')
    
    def update_variable_dict(self):
        self.variable_dict_new = update_variable_dict()
        with open(self.meta_dir + '/variable_dict.json', 'w') as f:
            json.dump(self.variable_dict_new, f)
        print('Success: Querier has updated variable dictionary!')

    def cmp_src_csv(self, nrows=None, var_list=None):
        self.read_csv_source_dict()
        self.read_variable_dict()
        cmp_src_csv(self.csv_source_dict, self.variable_dict, nrows=nrows, var_list=var_list)
 
    def create_csv_pool(self, csv_pool_dir=None, overwrite=False, source_key=None, file_key=None, sep="---"):
        import os
        if csv_pool_dir is None: # set default csv chunk pool dir
            csv_pool_dir = self.work_dir + '/csv_pool'
            if not os.path.exists(csv_pool_dir):
                os.mkdir(csv_pool_dir)
            else:
                if overwrite:
                    print('you are overwriting csv_pool in dir -- ' + csv_pool_dir)
                else: 
                    print(str(csv_pool_dir) + ' already exist, you can remove the folder or set overwrite=True')
                    return
        self.csv_pool_dir  = csv_pool_dir
        self.read_csv_source_dict()
        self.read_variable_dict()
        create_csv_pool(self.csv_source_dict, self.variable_dict, self.csv_pool_dir, source_key=source_key, file_key=file_key, sep=sep)
        
    