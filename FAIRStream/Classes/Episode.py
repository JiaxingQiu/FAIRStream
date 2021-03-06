""" Episode class. 

    Module description details:
    Episode object contains all the required definitions for a medical episode / episode of some outcome,
    before creating multivarable time series datasets, (flat dataframes or 3D TFDS), user must input 
    an episode definition by initiating an episode object.
    
    Usage example:

"""

class Episode:

    def __init__(self, input_time_len, output_time_len, time_unit=None, time_resolution=None, time_lag=None, anchor_gap=None):
        """ 
        initiate an episode object to set the definition of an episode for the time series study
    
        Arges:
            output_time_len: how many original time unit before an anchor (e.g 48*60 minutes)
            input_time_len: how many original time unit after an anchor (e.g 24*60 minutes)
            time_resolution: new resoluted unit of time, e.g every 15 minutes
            time_gap: minimum original time units between two episode anchors
        
        Returns:
            self attributes with corresponding names
        """

        if time_unit is None:
            time_unit = "(time unit not specified)"
        self.time_unit = str(time_unit)
        if time_resolution is None:
            time_resolution = 1
        if time_lag is None:
            time_lag = 0
        
        assert int(time_resolution)>0, "time resolution must be integar greater than 0"
        self.time_resolution = int(time_resolution)
        assert int(input_time_len)>0, "input time length must be integar greater than 0"
        self.input_time_len = int(input_time_len)
        assert int(output_time_len)>0, "output time length must be integar greater than 0"
        self.output_time_len = int(output_time_len)
        assert int(time_lag)>=0, "time lag/gap between last input and first output should be greater than or equal to 0"
        self.time_lag = int(time_lag)
        
        if anchor_gap is None:
            self.anchor_gap = self.input_time_len + self.time_lag + self.output_time_len
        else:
            self.anchor_gap = anchor_gap
        
        
    
    def __str__(self):
        return '\n'.join([
            f' ',
            f'An episode is defined to ',
            f'--- use {self.input_time_len} {self.time_unit}(s) long input variables ',
            f'--- predict {self.output_time_len} {self.time_unit}(s) response variables into the future',
            f'--- lag {self.time_lag} {self.time_unit}(s) between predictors and responses',
            f'--- increase by every {self.time_resolution} {self.time_unit}(s)',
            f'--- last at most {self.anchor_gap} {self.time_unit}(s) long'
        ])

        