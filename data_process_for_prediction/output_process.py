import pickle
import pandas as pd
import numpy as np

file_path = r'C:\Users\weijiexia\OneDrive - Delft University of Technology\Activites\tc_flow\KNMI_Data_Explore-\wind_generation_data\offshore_capacity.pkl'

def process_wind_data(file_path):
    with open(file_path, 'rb') as f:
        _data = pickle.load(f)
    # Only keep 'value_date_utc', 'value' columns
    _data = _data[['value_date_utc', 'value']]
    _value = _data['value'].values
    _value = _value[1:] - _value[:-1]
    _data = _data.iloc[1:]
    _data['value'] = _value
    return _data

data_offshore_capacity = process_wind_data(file_path)
print(data_offshore_capacity.head())

