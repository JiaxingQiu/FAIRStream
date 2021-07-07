""" MVTSConverter class. (Multi-Variate Time Series Data Converter class)

    Module description details:
    
    
    Usage example:

"""


from Class_Event import Event
from func_make_mvts_df import make_mvts_df, make_mvts_tfds

class MVTSConverter:
    
    def __init__(self, time_unit, time_before, time_after=None, time_resolution=None, time_gap=None):
        
        self.event = Event(time_unit, time_before, time_after, time_resolution, time_gap) # initiate an event object
        self.tfds = None
        self.df = None
    
    
    
    def dicts2df(self, uid_list, source_dict, variable_dict):
        
        self.df = make_mvts_df(uid_list, source_dict, variable_dict, self.event)

    
    
    def df2tfds(self, new_df=None):
        
        if new_df is not None:
            self.df = new_df # replace attritube self.df with new dataframe
        
        if self.df is None:
            return 'Warning: please input a dataframe object'
        
        self.tfds = make_mvts_tfds(self.df, self.event)
        