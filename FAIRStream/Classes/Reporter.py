from Functions import *
from Classes.Goblin import Goblin
from Functions.eval_mtrx_tfds import *

class Reporter(Goblin):
   def __init__(self, work_dir):
        Goblin.__init__(self, work_dir)
   
   def eval_mtrx_tfds(self, tfds, model):
      y, y_pred, eval_mtrx = eval_mtrx_tfds(tfds, model)
      return y, y_pred, eval_mtrx
   
   def eval_mtrx_tfds2(self, train_tfds, valid_tfds, model):
      _, _, eval_mtrx_train = eval_mtrx_tfds(train_tfds, model)
      _, _, eval_mtrx_valid = eval_mtrx_tfds(valid_tfds, model)
      
      return eval_mtrx_train, eval_mtrx_valid
