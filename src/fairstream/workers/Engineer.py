""" Engineer class. 2nd step in FAIR Medical AI framework, go through fucntionalities in data Engineering, following FAIR principle and 
    connecting to FAIRSCAPE web server.

    Module description details

    
    Usage example:

"""
from workers.Episode import Episode
from workers.Goblin import Goblin

from utils.make_mvts_df_from_csv_pool import *
from utils.make_mvts_tfds_from_df import *
import random


class Engineer(Goblin):

    def __init__(self, work_dir):
        Goblin.__init__(self, work_dir)
        self.read_csv_source_dict()
        self.read_sql_source_dict()
        self.read_variable_dict()
        self.episode = None
        self.sample_info = None
        self.mvts_df = None
        self.mvts_tfds = None

    def make_mvts_df_from_csv_pool(self, csv_pool_dir, nsbj=None, frac=0.3, viz=False, viz_ts=False, stratify_by=None):
        if self.episode is None:
            return 'No episode defined -- you can use Engineer.DefineEpisode() to define one'
        episode = self.episode
        self.mvts_df = make_mvts_df_from_csv_pool(csv_pool_dir, nsbj, frac, self.csv_source_dict, self.variable_dict, episode.input_time_len,
                                                  episode.output_time_len, episode.time_resolution, episode.time_lag, episode.anchor_gap, stratify_by=stratify_by, viz=viz, viz_ts=viz_ts)
        output_vars = []
        for var_dict in self.variable_dict.keys():
            if 'output' in self.variable_dict[var_dict].keys():
                if self.variable_dict[var_dict]['output']:
                    output_vars = output_vars + \
                        list(
                            self.mvts_df.columns[self.mvts_df.columns.str.startswith(str(var_dict))])
        assert len(
            output_vars) > 0, 'Engineer couldn\'t find output columns corresponding to the variable dictionary'
        input_vars = []
        for var_dict in self.variable_dict.keys():
            if 'input' in self.variable_dict[var_dict].keys():
                if self.variable_dict[var_dict]['input']:
                    input_vars = input_vars + \
                        list(
                            self.mvts_df.columns[self.mvts_df.columns.str.startswith(str(var_dict))])
        assert len(
            input_vars) > 0, 'Engineer couldn\'t find input columns corresponding to the variable dictionary'
        self.input_vars = input_vars
        self.output_vars = output_vars
        print("Success! Engineer has new attributes mvts_df, input_vars, output_vars. ")

    def make_mvts_tfds_from_df(self, mvts_df, batch_size=32):
        mvts_df = mvts_df[self.input_vars + self.output_vars]
        episode = self.episode
        mvts_tfds = make_mvts_tfds_from_df(mvts_df, input_vars=self.input_vars, output_vars=self.output_vars, input_time_len=episode.input_time_len,
                                           output_time_len=episode.output_time_len, time_resolution=episode.time_resolution, time_lag=episode.time_lag, batch_size=batch_size)
        return mvts_tfds

    def split_df(self, mvts_df=None, train_frac=0.8, byepisode=False):
        if mvts_df is not None:
            self.mvts_df = mvts_df
        if byepisode:
            self.mvts_df['split_id'] = self.mvts_df['__uid'].astype(
                str) + self.mvts_df['episode_order'].astype(str)
        else:
            self.mvts_df['split_id'] = self.mvts_df['__uid']
        all_list = list(self.mvts_df['split_id'].unique())
        random.shuffle(all_list)
        train_list = all_list[0:int(train_frac*len(all_list))]
        self.train_df = self.mvts_df[self.mvts_df['split_id'].isin(train_list)]
        self.valid_df = self.mvts_df[~self.mvts_df['split_id'].isin(
            train_list)]
        self.train_df = self.train_df.drop(columns=['split_id'])
        self.valid_df = self.valid_df.drop(columns=['split_id'])
        print("Success! Engineer has two new attributes train_df and valid_df. ")

    def fillna_by_train_df(self, train_df, valid_df, input_vars, output_vars, impute_input=None, impute_output=None, fill_value=-333):

        import missingno as msno
        # viz missingness
        print('--- Training MVTS DF missingness before imputation')
        msno.matrix(train_df, figsize=[15, 5], fontsize=10)
        plt.show()
        print('--- Validation MVTS DF missingness before imputation')
        msno.matrix(valid_df, figsize=[15, 5], fontsize=10)
        plt.show()

        train_df_imputed, valid_df_imputed = cohort_fillna(
            train_df=train_df, valid_df=valid_df, vars=input_vars, method=impute_input, fill_value=fill_value)
        train_df_imputed, valid_df_imputed = cohort_fillna(
            train_df=train_df_imputed, valid_df=valid_df_imputed, vars=output_vars, method=impute_output, fill_value=fill_value)
        self.train_df_imputed = train_df_imputed
        self.valid_df_imputed = valid_df_imputed
        # viz missingness
        print('--- Training MVTS DF missingness after imputation')
        msno.matrix(self.train_df_imputed, figsize=[15, 5], fontsize=10)
        plt.show()
        print('--- Validation MVTS DF missingness after imputation')
        msno.matrix(self.valid_df_imputed, figsize=[15, 5], fontsize=10)
        plt.show()
        print("Success! Engineer has two new attributes train_df_imputed and valid_df_imputed. ")

    def DefineEpisode(self, input_time_len, output_time_len, time_resolution=None, time_lag=None, anchor_gap=None):
        self.episode = Episode(input_time_len, output_time_len,
                               self.variable_dict['__time']['unit'], time_resolution=time_resolution, time_lag=time_lag, anchor_gap=anchor_gap)

    def BuildMVTS(self, csv_pool_dir, nsbj=None, frac=0.3, viz=False, viz_ts=False, stratify_by=None, train_frac=0.8, byepisode=False, batch_size=32, impute_input=None, impute_output=None, fill_value=-333, return_data=False):
        self.read_csv_source_dict()
        self.read_variable_dict()
        self.make_mvts_df_from_csv_pool(
            csv_pool_dir=csv_pool_dir, nsbj=nsbj, frac=frac, viz=viz, viz_ts=viz_ts, stratify_by=stratify_by)
        self.split_df(mvts_df=self.mvts_df,
                      train_frac=train_frac, byepisode=byepisode)
        self.fillna_by_train_df(self.train_df, self.valid_df, input_vars=self.input_vars, output_vars=self.output_vars,
                                impute_input=impute_input, impute_output=impute_output, fill_value=fill_value)

        self.train_tfds_imputed = self.make_mvts_tfds_from_df(
            self.train_df_imputed, batch_size=batch_size)
        self.valid_tfds_imputed = self.make_mvts_tfds_from_df(
            self.valid_df_imputed, batch_size=batch_size)
        print("Success! Engineer has new attributes train_tfds_imputed and valid_tfds_imputed. ")
        print(' ')
        print("\n--------------------------------- Engineer Attributes List -------------------------------\n")
        print(list(self.__dict__.keys()))
        print("\n----------------------------------------- Inputs -----------------------------------------\n")
        print(list(self.input_vars))
        print("\n----------------------------------------- Outputs ----------------------------------------\n")
        print(list(self.output_vars))
        print("\n------------------------------------- MVTS TFDS Shapes -----------------------------------\n")
        for example_inputs, example_labels in self.train_tfds_imputed.take(1):
            print(
                f'Inputs shape (batch size, time bins, variables): {example_inputs.shape}')
            print(
                f'Labels shape (batch size, time bins, variables): {example_labels.shape}')
        print("\n------------------------------------------------------------------------------------------\n")

        if return_data:
            return self.train_df_imputed, self.valid_df_imputed, self.train_tfds_imputed, self.valid_tfds_imputed
