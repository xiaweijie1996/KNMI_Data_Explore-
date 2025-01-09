import pickle
import matplotlib.pyplot as plt
import pandas as pd

file_path = r'wind_generation_data\point_carbon_wind_actual.pkl'

def load_wind_substract(file_path):
    with open(file_path, 'rb') as f:
        _data = pickle.load(f)
    # Only keep 'value_date_utc', 'value' columns
    _data = _data[['value_date_utc', 'value']]
    _value = _data['value'].values
    _value = _value[1:] - _value[:-1]
    _data = _data.iloc[1:]
    _data['value'] = _value
    return _data

def load_wind_read(file_path):
    with open(file_path, 'rb') as f:
        _data = pickle.load(f)
    _data = _data[['value_date_utc', 'value']]
    return _data

def _data_slice_date(data, start_date, end_date):
    """Slice data based on the data range"""
    return data[(data['value_date_utc'] >= start_date) & (data['value_date_utc'] <= end_date)]

def _data_look_back(data, look_back_step):
    """Process the data for prediction"""
    _data = data.copy()
    _data['value'] = _data['value'].shift(-look_back_step)
    _data.dropna(inplace=True)
    return _data

def data_process_auto_lookback(data, look_back_step_range = [1, 2, 5]):
    """Process the data for prediction"""
    new_data = data.copy()
   
    for _step in look_back_step_range:
        _data = _data_look_back(data, _step)
        new_data = pd.concat([new_data, _data['value']], axis=1)
    
    columns_name = ['value_lookback_'+str(_step) for _step in look_back_step_range]
    new_data.columns = ['value_date_utc', 'value'] + columns_name
    new_data.dropna(inplace=True)
    return new_data
   
if __name__ == "__main__":
    data = load_wind_read(file_path)
    data_look_back = data_process_auto_lookback(data)
    print('Data shape:', data.shape)

    # Plot the data
    plt.plot(data['value_date_utc'], data['value'])
    plt.title("Wind Generation Data")
    plt.show()