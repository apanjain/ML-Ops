import joblib
from sklearn.linear_model import LinearRegression
import logging
import pandas
import os

logging.basicConfig(filename=os.path.join(os.path.dirname(
    __file__), 'train-debug.log'), level=logging.INFO)

logging.info("Executing....")
# extract content of dataset in an array
try:
    ds = pandas.read_csv('salaryDataSet.csv')

# separate feature and target
    x = ds['YearsExperience'].values.reshape(30, 1)
    y = ds['Salary']

# train the model
    model = LinearRegression()
    model.fit(x, y)

# Dump the model using Joblib
    joblib.dump(model, 'model_dump')
    logging.info('model_dump created')
except Exception as e:
    logging.error(str(e))


logging.info("Program Quited!!!")
