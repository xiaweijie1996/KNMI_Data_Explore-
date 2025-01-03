import pickle
import pandas as pd
import numpy as np

# Read the data point_carbon_wind_actual.pkl
file_path = r'wind_data_explore\point_carbon_wind_actual.pkl'
with open(file_path, 'rb') as f:
    data_wind_actual = pickle.load(f)
print(data_wind_actual.head())

# Read the data onshore_capacity.pkl
file_path = r'wind_data_explore\onshore_capacity.pkl'
with open(file_path, 'rb') as f:
    data_onshore_capacity = pickle.load(f)
print(data_onshore_capacity.head())

# Read the data onshore_capacity.pkl
file_path = r'wind_data_explore\offshore_capacity.pkl'
with open(file_path, 'rb') as f:
    data_offshore_capacity = pickle.load(f)
print(data_offshore_capacity.head())