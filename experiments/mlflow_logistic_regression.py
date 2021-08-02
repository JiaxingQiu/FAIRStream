import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from urllib.parse import urlparse

import mlflow
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

df = pd.read_csv('toy_data/toydata.csv')

data = df.groupby('uid').agg(
    {
        'age': 'mean',
        'temperature': 'mean',
        'heart_rate': 'mean',
        'systolic_blood_pressure': 'mean',
        'diastolic_blood_pressure': 'mean',
        'resp_rate': 'mean',
        'y': lambda x: 1 if sum(x) > 0 else 0
    }
)

y = data['y']
X = data.drop('y', axis=1)

X: np.ndarray = SimpleImputer(strategy='mean').fit_transform(X)
y = y.to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

with mlflow.start_run():
    regr = LogisticRegression()
    regr.fit(X_train, y_train)

    rmse, mae, r2 = eval_metrics(y_test, regr.predict(X_test))
    score = regr.score(X_test, y_test)

    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)
    print("  ACC: %s" % score)

    mlflow.log_params(regr.get_params())

    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("acc", score)

    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

    # Model registry does not work with file store
    if tracking_url_type_store != "file":

        # Register the model
        # There are other ways to use the Model Registry, which depends on the use case,
        # please refer to the doc for more information:
        # https://mlflow.org/docs/latest/model-registry.html#api-workflow
        mlflow.sklearn.log_model(regr, "model", registered_model_name="LogRegModel")
    else:
        mlflow.sklearn.log_model(regr, "model")