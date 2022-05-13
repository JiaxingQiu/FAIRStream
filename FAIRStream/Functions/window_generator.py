import numpy as np
import tensorflow as tf

class WindowGenerator():
    def __init__(self, df, input_width, output_width, shift, stride, input_columns=None, output_columns=None):
        
        self.input_columns = input_columns
        self.output_columns = output_columns
        
        # Store the raw data.
        self.df = df[self.input_columns+self.output_columns] # output_columns need to be one-hot encoded
        
        # Work out the label column indices.
        if output_columns is not None:
            self.output_columns_indices = {name: i for i, name in enumerate(self.output_columns)}
            self.column_indices = {name: i for i, name in enumerate(self.df.columns)}

        # Work out the window parameters.
        self.input_width = input_width
        self.output_width = output_width
        self.shift = shift # steps of prediction made into the future
        self.stride = stride # period between sequences

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.output_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Input column name(s): {self.input_columns}',
            f'Label column name(s): {self.output_columns}'])

    def split_window(self, features):
        
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.input_columns is not None:
            inputs = tf.stack([inputs[:, :, self.column_indices[name]] for name in self.input_columns],axis=-1)
        if self.output_columns is not None:
            labels = tf.stack([labels[:, :, self.column_indices[name]] for name in self.output_columns],axis=-1)
        
        # Slicing doesn't preserve static shape information, so set the shapes
        # manually. This way the `tf.data.Datasets` are easier to inspect.
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.output_width, None])

        return inputs, labels
    
    def make_dataset(self, batch_size):
       
        data = np.array(self.df, dtype=np.float32)
        if data.shape[0] <= self.stride:
            nrow2pad = self.stride - data.shape[0] + 1
            data = np.append(data,np.zeros(shape=[nrow2pad,data.shape[1]]),0)

        ds = tf.keras.preprocessing.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=self.stride,
            shuffle=True,
            batch_size=batch_size)

        ds = ds.map(self.split_window)
        return ds


