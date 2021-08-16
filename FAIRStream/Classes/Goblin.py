""" Goblin class. 

Module description details
    
    Goblin is the parent class (initial role) for all the subclass players in FAIRstream workflow --
    Querier Engineer Learner Reporter -- to inherit. 
    
    All workers know (properties)
        meta_dir: where the dictionaries (cookbook) for the study
    
    All workers can (Functions)
        load_csv_source_dict: read source file dictionary
        load_variable_dict: read variables dictionary


    Usage example:

"""
import os
import json

class Goblin:
    
    def __init__(self, work_dir):
        self.work_dir = None
        self.meta_dir = None
        self.variable_dict = None
        self.csv_source_dict = None
        self.sql_source_dict = None
        
        # set study working directory
        self.work_dir = work_dir
        os.chdir(self.work_dir)
        # set dictionary folder under current working direction
        self.meta_dir = str(self.work_dir) + '/meta_data'
        if not os.path.exists(self.meta_dir):
            os.mkdir(self.meta_dir)
        
        return '\n'.join([
            f'Working directory: {self.work_dir}',
            f'Meta data path: {self.meta_dir}'
            ])
    
    

    def read_csv_source_dict(self, show=False):
        try:
            fullname = str(self.meta_dir)+'/csv_source_dict.json'
            f = open(fullname, "r")
            self.csv_source_dict = json.loads(f.read())
            if show:
                print(json.dumps(self.csv_source_dict, indent=2))
        except:
            print("Unable to read csv source dictionary. Use Querier.update_csv_source_dict() to build one.")
            return
    
    def read_sql_source_dict(self, show=False):
        try:
            fullname = str(self.meta_dir)+'/sql_source_dict.json'
            f = open(fullname, "r")
            self.sql_source_dict = json.loads(f.read())
            if show:
                print(json.dumps(self.sql_source_dict, indent=2))
        except:
            print("Unable to read sql source dictionary. Use Querier.update_sql_source_dict() to build one.")
            return
    
    def read_variable_dict(self, show=False):
        try:
            fullname = str(self.meta_dir)+'/variable_dict.json'
            f = open(fullname, "r")
            self.variable_dict = json.loads(f.read())
            if show:
                print(json.dumps(self.variable_dict, indent=2))
        except:
            print("Unable to read variable dictionary. Use Querier.update_variable_dict() to build one.")
            return
        




        