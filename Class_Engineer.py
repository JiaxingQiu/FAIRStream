""" Engineer class. 2nd step in FAIR Medical AI framework, go through fucntionalities in data Engineering, following FAIR principle and 
    connecting to FAIRSCAPE web server.

    Module description details

    
    Usage example:

"""

import random

from func_set_uid import set_uid
from Class_MVTSConverter import MVTSConverter
from Class_MediWorker import MediWorker

class Engineer(MediWorker):
    
    def __init__(self, wd):
        MediWorker.__init__(self, wd)
        MediWorker.load_source_dict(self)
        MediWorker.load_variable_dict(self)
        self.uid_pool = None
        self.uid_drop = None
    
    def __str__(self):
        base_info = [
            f'Engineer can prepare data for multivariate time series modeling!',
            f'    clean flat time series dataframe for Machine Learning models',
            f'    clean 3D TFDS object for multivariable time series Deep Learning models',
            f'Engineer has attributes: ',
            f'    {self.__dict__.keys()}']
        if self.source_dict is None:
            massage_list = [
                f'Engineer cannot load source file dictionary from: {self.dict_folder_path}',
                f'    You can use querier.update_source_dict() to build one'
            ]
            return '\n'.join(base_info + massage_list) 
        if self.variable_dict is None:
            massage_list = [
                f'Engineer cannot load existed variable file dictionary in current working directory: {self.dict_folder_path}',
                f'    You can use querier.update_variable_dict() to build one'
            ]
            return '\n'.join(base_info + massage_list) 
        return '\n'.join( base_info + [
            f'Engineer is working with dictionaries with below elements',
            f'    sources: {[key for key in self.source_dict.keys()]}',
            f'    variables: {[key for key in self.variable_dict.keys()]}'
        ]) 
   
    
    def set_uid(self, warning=False):
        """ 
        Details: 
            Engineer object function: set_uid to set unique id for a study 
        Arges:
            self: engineer object
            warning: whether or not print warning messages 
        Returns:
            new attributes to engineer object -- uid_pool, uid_drop
        """
        print('---- Engineer is preparing unique subject id for the study! ----\n')
        self.uid_pool, self.uid_drop = set_uid(self.source_dict, warning)
        print('---- Success: Engineer has new attributes -- uid_pool, uid_drop ----\n')
    
    def get_uid(self):
        """ 
        Details: 
            Engineer object function: get_uid to print detailed information about unique id for a study 
        Arges:
            self: engineer object
        Returns:
        """
        return '\n'.join([
            f'Numebr of included subjects: {str(len(self.uid_pool))}',
            f'Number of excluded subjects: {str(len(self.uid_drop))}',
            f'included uid: {self.uid_pool}',
            f'excluded uid: {self.uid_drop}'
            ])

        
    def subset_uid(self, nsbj):
        print('---- Engineer is sampling study subjects ----\n')
        if self.uid_pool is None:
            return 'Warning: unique study subject id not exist, please use Engineer.set_uid() to create one' # check uid_pool
        self.uid_subset = random.sample(self.uid_pool, min(int(nsbj),len(self.uid_pool)))
        print(f'{len(self.uid_subset)} subjects are sampled from {len(self.uid_pool)} population without replacement \n')
        print('---- Success: Engineer has new attributes -- uid_subset ----\n')
   
    
    def build_mvts_data(self, nsbj, time_before, time_after=None, time_resolution=None, time_gap=None):
        """ 
        init_mvts is a within-class function for engineer: 
        initiate multivariate time series data frame (flat table) for ML and DL
    
        Arges:
            nsbj: number of subjects in a subset sample
            return_df: whether or not return dataframe object
        
        Returns:
            add new attributes to mvts
        """

        print('---- Engineer is creating multivariate time series dataframe and 3D tenserflow dataset ----\n')
        # 1. initiate a mvts object
        self.mvts = MVTSConverter(str(self.variable_dict['time']['attr']['unit']), time_before, time_after, time_resolution, time_gap)
        # 2. sample from population
        self.subset_uid(nsbj)
        # 3. make data frame format / flat table of multivariate time series
        self.mvts.dicts2df(self.uid_subset, self.source_dict, self.variable_dict)
        # 4. convert to tfds
        self.mvts.df2tfds()
        print('---- Success: Engineer has new attributes -- mvts.df, mvts.tfds ----\n')
        