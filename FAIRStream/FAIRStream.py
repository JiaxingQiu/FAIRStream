""" 

Module description details
   
    Usage example:

"""

from Classes.Engineer import Engineer
from Classes.Querier import Querier
from Classes.Learner import Learner
from Classes.Reporter import Reporter

class FAIRStream:
    
    def __init__(self, work_dir):
        self.querier = Querier(work_dir)
        self.engineer = Engineer(work_dir)
        self.learner = Learner(work_dir)
        self.reporter = Reporter(work_dir)
