import openmeteo_requests
import pickle
import requests_cache
import pandas as pd
from retry_requests import retry
from tqdm import tqdm

# All available weather variables
full_variables = ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", 
            "precipitation", "rain", "snowfall", "weather_code", "pressure_msl", "surface_pressure", 
            "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", 
            "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_50m", 
            "wind_speed_100m", "wind_speed_200m", "wind_speed_300m", "wind_direction_10m", "wind_direction_50m",
            "wind_direction_100m", "wind_direction_200m", "wind_direction_300m", "wind_gusts_10m", 
            "surface_temperature", "temperature_50m", "temperature_100m", "temperature_200m", "temperature_300m"]

def _get_order_num_of_variable(variables):
    
    """ Get the order of variables which are listed in the full_variables, 
    eg, ["temperature_2m", "relative_humidity_2m"] will return [0, 1]
   """
   
    _index_list = []
    for i in variables:
        _index_list.append(full_variables.index(i))
    return _index_list

def _get_gird(gird_shape = (20, 20)):
    
    """ Load the grid from the pickle file, and divide the grid into 20*20 small grids, 
    this function will return a list of small grids which is used to get the historical 
    weather data and the small grid will leads to a smaller computing time.
    
    eg. if the grid is 130*130, the return value will be a list of (20, 20) small grids.
    """
    
    _pickle_path = r'grid.pkl'
    with open(_pickle_path, 'rb') as f:
        grid = pickle.load(f)
    latitude_max = grid["latitude"].max()
    latitude_min = grid["latitude"].min()
    longitude_max = grid["longitude"].max()
    longitude_min = grid["longitude"].min()
    
    # Divide the grid into 20*20
    latitude_interval = (latitude_max - latitude_min) / gird_shape[0]
    longitude_interval = (longitude_max - longitude_min) / gird_shape[1]
    
    # Create a grid
    new_latitude = [latitude_min + i * latitude_interval for i in range(gird_shape[0] + 1)]
    new_longitude = [longitude_min + i * longitude_interval for i in range(gird_shape[1] + 1)]
    new_grid = {"latitude": new_latitude, "longitude": new_longitude}
    
    # Iteratively pair the latitude and longitude
    new_grid_list = []
    for i in range(gird_shape[0]):
        for j in range(gird_shape[1]):
            new_grid_list.append((new_latitude[i], new_longitude[j]))
            
    return new_grid_list


# Get the historical weather data from AIP
def get_weather_data(location, # (latitude, longitude)
                                variables, # vaiables to be extracted
                                data_range = None, # date range, eg ("2024-12-19", "2025-01-01")
                                models = "knmi_harmonie_arome_netherlands"
                                ):
    
    """ Get the historical weather data from the Open-Meteo API, based on the location, variables, and date range."""
    
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    if data_range is None:
        url =  "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": location[0],
            "longitude": location[1],
            # "start_date": data_range[0],
            # "end_date": data_range[1],
            "hourly": variables,
            "models": models
        }
    else:
        url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
        params = {
            "latitude": location[0],
            "longitude": location[1],
            "start_date": data_range[0],
            "end_date": data_range[1],
            "hourly": variables,
            "models": models
        }
    
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    
    # Get the order of variables
    keys_of_variable = _get_order_num_of_variable(variables)
    
    # Create a dataframe to store the data
    hourly = response.Hourly()
    
    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    
    for _order in range(len(keys_of_variable)):
        _data = hourly.Variables(keys_of_variable[_order]).ValuesAsNumpy()
        hourly_data[variables[_order]+f'-{location}'] = _data
    
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    
    return hourly_dataframe


def get_grid_weather_data(grid_list,
                         variables, # vaiables to be extracted
                         data_range = None, # date range, eg ("2024-12-19", "2025-01-01")
                         models = "knmi_harmonie_arome_netherlands"):
    
    """ Get the historical weather data of each grid point from the Open-Meteo API, based on the variables and date range."""
    
    _collected_dataframes = []
    for _grid in tqdm(grid_list):
        _dataframe = get_weather_data(_grid, variables, data_range, models)
        _collected_dataframes.append(_dataframe)
        _collected_dataframes[-1].index = _collected_dataframes[-1]['date']
        _collected_dataframes[-1].drop(columns = 'date', inplace = True)
        
    _collected_dataframes = pd.concat(_collected_dataframes, axis = 1)
    return _collected_dataframes

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    _grid_shape = (130, 130)
    for i in range(len(full_variables)):
        
        collected_data = get_grid_weather_data(_get_gird(_grid_shape), full_variables[i:i+1], None)
        print(full_variables[i])
        _row = collected_data.iloc[0,:].values
        _row = _row.reshape(_grid_shape).T
        plt.imshow(_row)
        
        break