""" Event class. 

    Module description details:
    Event object contains all the required definitions for a medical episode / event of some outcome,
    before creating multivarable time series datasets, (flat dataframes or 3D TFDS), user must input 
    an event definition by initiating an event object.
    
    Usage example:

"""

class Event:

    def __init__(self, time_unit, time_before, time_after=None, time_resolution=None, time_gap=None):
        """ 
        initiate an event object to set the definition of an event for the time series study
    
        Arges:
            time_before: how many original time unit before an outcome (e.g 48*60 minutes)
            time_after: how many original time unit after an outcome (e.g 24*60 minutes)
            time_resolution: new resoluted unit of time, e.g every 15 minutes
            time_gap: minimum original time units between two events
        
        Returns:
            self attributes with corresponding names
        """
        self.time_unit = str(time_unit)
        self.time_before = int(time_before)
        if time_after is not None:
            self.time_after = int(time_after)
        else:
            self.time_after = 0
        if time_resolution is not None:
            self.time_resolution = int(time_resolution)
            if self.time_after != 0:# check time_after for predictive modeling
                print('  warning: you are including data after an outcome')
        else:
            self.time_resolution = 1
        if time_gap is not None:
            self.time_gap = time_gap
        else:
            self.time_gap = self.time_before + self.time_after
        print('\n'.join([
            f' ',
            f'An event is defined to - ',
            f'    - have {self.time_before} {self.time_unit}s before an outcome',
            f'    - have {self.time_after} {self.time_unit}s after an outcome',
            f'    - increase by every {self.time_resolution} {self.time_unit}s',
            f'    - keep an outcome at least {self.time_gap} {self.time_unit}s apart from the last one',
            f' '
        ]))
        