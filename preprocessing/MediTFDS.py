""" MediTFDS processor object.

Module description details...

    Usage example:

"""
import dictionaries
from prep_id_pool import prep_id_pool
from prep_id_subset import prep_id_subset
import proc_md2tfds_cohort

class MediTFDSGenerator:
    def __init__(self):
        
        self.source_dict = dictionaries.source_dict
        self.variable_dict = dictionaries.variable_dict
        

    def __str__(self):
        return '\n'.join([
            f'Sources: {[key for key in self.source_dict.keys()]}',
            f'Variables: {[key for key in self.variable_dict.keys()]}'
            ])


    def PrepareTables(self, nsbj=None):
        if nsbj is None:
            self.nsbj = 300
        else:
            self.nsbj = nsbj # defualt numebr of subjects to sample
        
        # step 1: prep_id_pool
        self.id_pool = prep_id_pool(self.source_dict)

        # step 2: prep_id_subset
        self.id_list = prep_id_subset(self.id_pool, self.nsbj)


    def ProcessMD2TD(self, vars_include=None, time_bin=None, time_unit_before=None, time_unit_after=None):
        
        if vars_include is None:
            self.vars_include = []
        else:
            self.vars_include = vars_include

        if time_bin is None:
            self.time_bin = 1
        else:
            self.time_bin = time_bin

        if time_unit_before is None:
            self.time_unit_before = 33
        else:
            self.time_unit_before = time_unit_before

        if time_unit_after is None:
            self.time_unit_after = 0
        else:
            self.time_unit_after = time_unit_after

        self.dataset = proc_md2tfds_cohort(self.id_list, self.vars_include, self.source_dict, self.variable_dict, self.time_bin, self.time_unit_before, self.time_unit_after)
