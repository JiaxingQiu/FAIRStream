""" Engineer class. 2nd step in FAIR Medical AI framework, go through fucntionalities in data Engineering, following FAIR principle and 
    connecting to FAIRSCAPE web server.

    Module description details

    
    Usage example:

"""
from Functions.make_mvts_df_from_csv_pool import *
from Functions.cohort_fillna import *
from Functions.make_mvts_tfds_from_df import *
from Functions.extract_xy import *
from Classes.Goblin import Goblin
from Classes.Episode import Episode
import random


class Engineer(Goblin):
    
    def __init__(self, work_dir):
        Goblin.__init__(self, work_dir)
        self.read_csv_source_dict()
        self.read_sql_source_dict()
        self.read_variable_dict()
        self.input_vars = None
        self.output_vars = None
        self.episode = None
        self.sample_info = None
        self.mvts_df = None
        self.mvts_tfds = None
        self.train_df = None
        self.valid_df = None
        self.test_df = None
        self.train_df_imputed = None
        self.valid_df_imputed = None
        self.test_df_imputed = None
        self.train_tfds = None
        self.valid_tfds = None
        self.test_tfds = None

    def info(self):
        print("\n----------------------------- Engineer Attributes List ------------------------\n")
        print(list(self.__dict__.keys()))
        print("\n------------------------------------- Inputs  --------------------------------- \n")
        print(list(self.input_vars))
        print("\n------------------------------------- Outputs --------------------------------- \n")
        print(list(self.output_vars)) 
        try:
            print("\n------------------ train_tfds / valid_tfds / test_tfds batch shape --------------\n")
            for example_inputs, example_labels in self.train_tfds.take(1):
                print(f'Inputs shape (batch size, time bins, variables): {example_inputs.shape}')
                print(f'Labels shape (batch size, time bins, variables): {example_labels.shape}')
        except:
            pass
        try:
            print("\n---------------------- train_df / train_df_imputed shape ---------------------- \n")
            print(self.train_df.shape)
        except:
            pass
        try:
            print("\n---------------------- valid_df / valid_df_imputed shape ---------------------- \n")
            print(self.valid_df.shape)
        except:
            pass
        try:
            print("\n------------------------ test_df / test_df_imputed shape ---------------------- \n")
            print(self.test_df.shape)
        except:
            pass
       
        
         
    def make_mvts_df_from_csv_pool(self, csv_pool_dir, nsbj=None, frac=0.3, topn_eps=None, viz=False, viz_ts=False, stratify_by=None, dummy_na=False):
        if self.episode is None:
            return 'No episode defined -- you can use Engineer.DefineEpisode() to define one'
        episode = self.episode
        self.mvts_df = make_mvts_df_from_csv_pool(csv_pool_dir, nsbj, frac, self.csv_source_dict, self.variable_dict, episode.input_time_len, episode.output_time_len, episode.time_resolution, episode.time_lag, episode.anchor_gap, stratify_by=stratify_by, viz=viz, viz_ts=viz_ts, dummy_na=dummy_na, topn_eps=topn_eps)
        output_vars = []
        for var_dict in self.variable_dict.keys():
            if 'output' in self.variable_dict[var_dict].keys():
                if self.variable_dict[var_dict]['output']:
                    output_vars = output_vars + list(self.mvts_df.columns[self.mvts_df.columns.str.startswith(str(var_dict))])
        assert len(output_vars)>0, 'Engineer couldn\'t find output columns corresponding to the variable dictionary'
        input_vars = []
        for var_dict in self.variable_dict.keys():
            if 'input' in self.variable_dict[var_dict].keys():
                if self.variable_dict[var_dict]['input']:
                    input_vars = input_vars + list(self.mvts_df.columns[self.mvts_df.columns.str.startswith(str(var_dict))])
        assert len(input_vars)>0, 'Engineer couldn\'t find input columns corresponding to the variable dictionary'
        self.input_vars = input_vars
        self.output_vars = output_vars
        # coordinate column name orders
        base_vars = list(self.mvts_df.columns[~self.mvts_df.columns.isin(self.input_vars+self.output_vars)])
        self.mvts_df = self.mvts_df[self.input_vars+self.output_vars+base_vars] # mvts_df is not imputed
        print("Success! Engineer has updated attributes --- mvts_df, input_vars, output_vars. ")

     
       
    def split_df(self, mvts_df=None, valid_frac=0, test_frac=0, byepisode=False):
        if mvts_df is not None:
            self.mvts_df = mvts_df
        if byepisode:
            self.mvts_df['split_id'] = self.mvts_df['__uid'].astype(str) + self.mvts_df['episode_order'].astype(str)
        else:
            self.mvts_df['split_id'] = self.mvts_df['__uid']
        all_list = list(self.mvts_df['split_id'].unique())
        random.shuffle(all_list)

        assert valid_frac>=0 and valid_frac<1, "validation set fraction must be >=0 and <1"
        assert test_frac>=0 and test_frac<1, "test set fraction must be >=0 and <1"
        train_frac = 1-valid_frac-test_frac
        assert train_frac>0 and train_frac<=1, "train set fraction must be >0 and <=1, please input legit valid_frac and/or test_frac"
        
        train_list = all_list[0:int(train_frac*len(all_list))]
        self.train_df = self.mvts_df[self.mvts_df['split_id'].isin(train_list)]
        self.train_df = self.train_df.drop(columns=['split_id'])
        
        if valid_frac > 0:
            valid_list = all_list[int(train_frac*len(all_list)):int((train_frac+valid_frac)*len(all_list))]
            self.valid_df = self.mvts_df[self.mvts_df['split_id'].isin(valid_list)]
            self.valid_df = self.valid_df.drop(columns=['split_id'])

        if test_frac > 0:
            test_list = all_list[int((train_frac+valid_frac)*len(all_list)):int(len(all_list))]
            self.test_df = self.mvts_df[self.mvts_df['split_id'].isin(test_list)]
            self.test_df = self.test_df.drop(columns=['split_id'])
        print("Success! Engineer has updated attributes --- train_df, valid_df and test_df. ")
    
    def cohort_fillna(self, impute_input=None, impute_output=None, fill_value=-333, viz=True):
        if self.train_df is not None:
            self.train_df_imputed = cohort_fillna(refer_df=self.train_df, df=self.train_df, vars=self.input_vars, method=impute_input, fill_value=fill_value, viz=viz)
            self.train_df_imputed = cohort_fillna(refer_df=self.train_df, df=self.train_df_imputed, vars=self.output_vars, method=impute_output, fill_value=fill_value, viz=viz)
            
            if self.valid_df is not None:
                self.valid_df_imputed  = cohort_fillna(refer_df=self.train_df, df=self.valid_df, vars=self.input_vars, method=impute_input, fill_value=fill_value, viz=viz)
                self.valid_df_imputed  = cohort_fillna(refer_df=self.train_df, df=self.valid_df_imputed , vars=self.output_vars, method=impute_output, fill_value=fill_value, viz=viz)
                
            if self.test_df is not None:
                self.test_df_imputed = cohort_fillna(refer_df=self.train_df, df=self.test_df, vars=self.input_vars, method=impute_input, fill_value=fill_value, viz=viz)
                self.test_df_imputed = cohort_fillna(refer_df=self.train_df, df=self.test_df_imputed, vars=self.output_vars, method=impute_output, fill_value=fill_value, viz=viz)
                
        print("Success! Engineer has updated attributes --- train_df_imputed, valid_df_imputed and test_df_imputed. ")
    
    def DefineEpisode(self, input_time_len, output_time_len, time_resolution=None, time_lag=None, anchor_gap=None):
        self.episode = Episode(input_time_len, output_time_len, self.variable_dict['__time']['unit'], time_resolution=time_resolution, time_lag=time_lag, anchor_gap=anchor_gap)
        print("Success! Engineer has updated attributes --- episode. ")
    
    def BuildMVTS(self, csv_pool_dir, nsbj=None, frac=0.3, viz=False, viz_ts=False, stratify_by=None, valid_frac=0, test_frac=0, byepisode=False, batch_size=32, impute_input=None, impute_output=None, fill_value=-333, dummy_na=False, topn_eps=None):
        self.read_csv_source_dict()
        self.read_variable_dict()
        self.make_mvts_df_from_csv_pool(csv_pool_dir=csv_pool_dir, nsbj=nsbj, frac=frac, viz=viz, viz_ts=viz_ts, stratify_by=stratify_by, dummy_na=dummy_na, topn_eps=topn_eps)
        self.split_df(mvts_df=self.mvts_df, valid_frac=valid_frac, test_frac=test_frac, byepisode=byepisode)
        self.cohort_fillna(impute_input=impute_input, impute_output=impute_output, fill_value=fill_value, viz=viz)
        
        if self.train_df_imputed is not None:
            self.train_tfds = make_mvts_tfds_from_df(self.train_df_imputed, input_vars=self.input_vars, output_vars=self.output_vars, input_time_len=self.episode.input_time_len, output_time_len=self.episode.output_time_len, time_resolution=self.episode.time_resolution, time_lag=self.episode.time_lag, batch_size=batch_size)
        if self.valid_df_imputed is not None:
            self.valid_tfds = make_mvts_tfds_from_df(self.valid_df_imputed, input_vars=self.input_vars, output_vars=self.output_vars, input_time_len=self.episode.input_time_len, output_time_len=self.episode.output_time_len, time_resolution=self.episode.time_resolution, time_lag=self.episode.time_lag, batch_size=batch_size)
        if self.test_df_imputed is not None:
            self.test_tfds = make_mvts_tfds_from_df(self.test_df_imputed, input_vars=self.input_vars, output_vars=self.output_vars, input_time_len=self.episode.input_time_len, output_time_len=self.episode.output_time_len, time_resolution=self.episode.time_resolution, time_lag=self.episode.time_lag, batch_size=batch_size)
        
        print("Success! Engineer has updated attributes --- train_tfds, valid_tfds and test_tfds. ")
        
    def ExtractXY(self, shape_type="3d"):
        X_train=None
        Y_train=None
        X_valid=None
        Y_valid=None
        X_test=None
        Y_test=None
        
        X_train, Y_train = extract_xy(self.train_tfds, shape_type)
        X_valid, Y_valid = extract_xy(self.valid_tfds, shape_type)
        X_test, Y_test = extract_xy(self.test_tfds, shape_type)
        
        return X_train, Y_train, X_valid, Y_valid, X_test, Y_test

        


        