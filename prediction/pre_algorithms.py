import sys
import os
path = os.getcwd()
sys.path.append(os.path.abspath(path))

from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt

import data_process_for_prediction.output_process as op

file_path = r'C:\Users\weijiexia\OneDrive - Delft University of Technology\Activites\tc_flow\KNMI_Data_Explore-\wind_generation_data\point_carbon_wind_actual.pkl'

_list = [i for i in range(12, 48)]
X = op.data_process_auto_lookback(op.load_wind_read(file_path), _list)
y = X['value']
X_input = X.drop(columns=['value_date_utc', 'value'])

# Train the model
data_num = 1000
regr = RandomForestRegressor(max_depth=5, random_state=0)
regr.fit(X_input[:data_num].values, y[:data_num].values)

# Make prediction
gap = 400
y_hat = regr.predict(X_input[data_num:data_num+gap].values)

# Plot the prediction
# Figure size (10, 5)
plt.figure(figsize=(10, 5))
plt.plot(X['value_date_utc'][data_num:data_num+gap], y_hat, label='Prediction')
plt.plot(X['value_date_utc'][data_num:data_num+gap], y[data_num:data_num+gap].values, label='Actual')
plt.title("Wind Generation Data")
plt.legend()
plt.show()
