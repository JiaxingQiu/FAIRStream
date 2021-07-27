""" FAIRStream module.  Working flow / environment object for MediAI working objects in a multivariable time series medical ML study/research

Module description details
   
    Usage example:

"""

from workers.Querier import Querier
from workers.Engineer import Engineer
from workers.Learner import Learner
from workers.Reporter import Reporter

class FAIRStream:
    
    def __init__(self, work_dir):
        self.querier = Querier(work_dir)
        self.engineer = Engineer(work_dir)
        self.learner = Learner(work_dir)
        self.reporter = Reporter(work_dir)
