# FAIRStream

### About this package
* FAIRStream is a Data Science software, integrating FAIR principle with Data Science / Machine Learning life cycle. The software is developed to automate Multi-Variate Time Series Data Analysis, Statistical Modeling and Deep Leaning processes in most Medical studies with longitudinal data. 
* Language: Python, R, SQL

![alt text](https://github.com/UVA-CAMA/FAIRStream/blob/main/resources/poster.png)

### Data Querying and Data Engineering
* CSV API Overview: 
  * [1] **Create stuty csv pool**: loop through all source files listed in source dictionary, create a csv pool folder containing multiple csv files, one per each subject. *Main function --  FAIRStream.querier.create_csv_pool()*
  * [2] **Sampling subset subject cohort**: for studies involving large subject population, subset subject cohort by a certain sample size or fraction, use bootstrapping without replacement, read sampled subject csvs by file name. *Main function -- FAIRStream.engineer.make_mvts_df_from_csv()*
  * [3] **Feature engineering**: based on variable dictionary, uniform variable names, fix dtype and outliers, merge seperate files from a same patient by time and uid, customise imputation methods, return one numeric Multi-Variate Time Series event chunks table, that is ready for machine learning approaches. *Main function: FAIRStream.engineer.make_mvts_df_from_csv()* 
  * [4] **Train test dataset split**: split training and testing dataframe by given fraction ratio and spliting type (event-wise or subject-wise). *Main function: FAIRStream.engineer.train_val_split_df()*
  * [5] **Convert DataFrames to TFDS**: convert dataframes of any size to a 3D Multi-Variate Time Series TensorFlow Dataset. *Main function: FAIRStream.engineer.make_mvts_tfds_from_df()*

![alt text](https://github.com/UVA-CAMA/FAIRStream/blob/main/resources/csv_api.png)
