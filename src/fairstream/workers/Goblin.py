""" Goblin class. 

Module description details
    
    Goblin is the parent class (initial role) for all the subclass players in FAIRstream workflow --
    Querier Engineer Learner Reporter -- to inherit. 
    
    All workers know (properties)
        meta_dir: where the dictionaries (cookbook) for the study
    
    All workers can (functions)
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
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)
        # os.chdir(self.work_dir)
        # set dictionary folder under current working direction
        self.meta_dir = os.path.join(self.work_dir, 'metadata')
        if not os.path.exists(self.meta_dir):
            os.mkdir(self.meta_dir)

        return '\n'.join([
            f'Working directory: {self.work_dir}',
            f'Meta data path: {self.meta_dir}'
        ])

    """
    @name: Zack
    @email: zwb6kg@virginia.edu

    BUG: This bug is pretty serious.
    The Querier class uses the Goblin class' constructor to initialize itself.
    Once it is initialized, it initializes the csv_source_dict and the variable_dict.
    However, it initializes the variable_dict into an object called variable_dict_demo.
    The variable_dict variable is initialized to None in the engineer, by the Goblin's constructor.
    Then, the Querier is called to update the csv_source_dict and the variable_dict,
    but these changes are never brought into the engineer.
    So when the engineer calls its DefineEpisode method, it tries to access the variable_dict, which is still None.
    This causes an error, and exits the program with the following Error:

    File "C:\Users\Zack-UVA\Documents\FAIRStream\src\fairstream\workers\Engineer.py", line 112, in DefineEpisode
        self.variable_dict['__time']['unit'], time_resolution=time_resolution, time_lag=time_lag, anchor_gap=anchor_gap)
    TypeError: 'NoneType' object is not subscriptable

    This error is fixable in two ways:
        1. Update the csv_source_dict and the variable_dict in the Querier's constructor.
        2. Read the updated csv_source_dict and the variable_dict into the Engineer *after* they have been updated.

    The first way does not allow the user to manually input their variables, and initializes them to whatever is inside prep_dicts.py.
    The second way requires the user to write extra code that they may not understand, and may result in frustration later on.

    In my personal opinion, we need to rethink the prep_dicts.py file. 
    I think that it is not good practice to have entire dictionaries defined inside the prep_dicts.py file.
    We should extract those into json files, and have the prep_dicts.py file read those json files.
    That way, we can write code to have users generate those json files with all of their variables,
    and have a better flow of data through the program.
    """

    def read_csv_source_dict(self, show=False):
        try:
            fullname = os.path.join(self.meta_dir, 'csv_source_dict.json')
            f = open(fullname, "r")
            self.csv_source_dict = json.loads(f.read())
            if show:
                print(json.dumps(self.csv_source_dict, indent=2))
        except:
            print(
                "Unable to read csv source dictionary. Use Querier.update_csv_source_dict() to build one.")
            return

    def read_sql_source_dict(self, show=False):
        try:
            fullname = os.path.join(self.meta_dir, 'sql_source_dict.json')
            f = open(fullname, "r")
            self.sql_source_dict = json.loads(f.read())
            if show:
                print(json.dumps(self.sql_source_dict, indent=2))
        except:
            print(
                "Unable to read sql source dictionary. Use Querier.update_sql_source_dict() to build one.")
            return

    def read_variable_dict(self, show=False):
        try:
            fullname = os.path.join(self.meta_dir, 'variable_dict.json')
            f = open(fullname, "r")
            self.variable_dict = json.loads(f.read())
            if show:
                print(json.dumps(self.variable_dict, indent=2))
        except:
            print(
                "Unable to read variable dictionary. Use Querier.update_variable_dict() to build one.")
            return
