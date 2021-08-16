import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import r2_score


def eval_mtrx_tfds(tfds, model):
    """ 
    evaluation matrix for tfds version model results per column / per variable

    Arges:
        tfds: test/validation tfds data used for evaluation a deep learning model
        model: a deep learning / keras model object
    
    Returns:
        an evaluation matrix dataframe combined of ones per variable in a test set
        y
        y_pred
        eval_mtrx
    """
    
   
    # reshape tfds -- inverse time dimension into rows
    batch_count = [i for i,_ in enumerate(tfds)][-1] + 1
    y = None
    for _, y_batch in tfds.take(batch_count):
        print(f'current batch of testing tfds shape (batch_size, time, variables): {y_batch.shape}' )
        y_batch_array = np.array(y_batch).reshape((int(y_batch.shape[0]*y_batch.shape[1]),y_batch.shape[-1]))
        if y is None:
            y = y_batch_array
        else:
            y = np.concatenate((y, y_batch_array), axis=0) 
    print(f'Success! 2D reponse data --- y --- has shape: {y.shape}')
    
    # reshape test_pred
    y_pred = model.predict(tfds)
    y_pred = y_pred.reshape((y_pred.shape[0]*y_pred.shape[1],y_pred.shape[-1]))
    print(f'Success! 2D resposne data --- y_pred --- has shape: {y_pred.shape}')
    
    # generate evaluation matrix
    eval_mtrx = pd.DataFrame()
    for i in range(y.shape[-1]):

        eval_mtrx_var = pd.DataFrame({
            'response':['variable '+str(i+1)],
            'auc': [float(roc_auc_score(y[:,i], y_pred[:,i]))],
            'r2': [float(r2_score(y[:,i], y_pred[:,i]))]
        })
        eval_mtrx = pd.concat([eval_mtrx, eval_mtrx_var],sort=False)
    
    eval_mtrx = eval_mtrx.reset_index(drop=True)

    return y, y_pred, eval_mtrx
