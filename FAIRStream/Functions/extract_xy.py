import numpy as np

def extract_xy(tfds, shape_type="3d"): 
    X = None
    Y = None
    try:
        batch_count = [i for i,_ in enumerate(tfds)][-1] + 1
        for x_batch, y_batch in tfds.take(batch_count):
            
            if shape_type == 'df':
                X_batch_array = np.array(x_batch).reshape((int(x_batch.shape[0]*x_batch.shape[1]),x_batch.shape[2]))
                y_batch_array = np.array(y_batch).reshape((int(y_batch.shape[0]*y_batch.shape[1]),y_batch.shape[2]))
            elif shape_type == '3d':
                X_batch_array = np.array(x_batch)
                y_batch_array = np.array(y_batch)
            elif shape_type == '2d':
                X_batch_array = np.array(x_batch).reshape((int(x_batch.shape[0]),int(x_batch.shape[1]*x_batch.shape[2])))
                y_batch_array = np.array(y_batch).reshape((int(y_batch.shape[0]),int(y_batch.shape[1]*y_batch.shape[2])))
            
            if X is None:
                X = X_batch_array
            else:
                X = np.concatenate((X, X_batch_array), axis=0) 
            if Y is None:
                Y = y_batch_array
            else:
                Y = np.concatenate((Y, y_batch_array), axis=0) 
    except:
        pass
    return X,Y
