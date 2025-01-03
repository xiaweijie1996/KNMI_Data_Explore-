import openmeteo_requests
import pickle
import requests_cache
import pandas as pd
from retry_requests import retry
from tqdm import tqdm

full_variables = ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", 
            "precipitation", "rain", "snowfall", "weather_code", "pressure_msl", "surface_pressure", 
            "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", 
            "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_50m", 
            "wind_speed_100m", "wind_speed_200m", "wind_speed_300m", "wind_direction_10m", "wind_direction_50m",
            "wind_direction_100m", "wind_direction_200m", "wind_direction_300m", "wind_gusts_10m", 
            "surface_temperature", "temperature_50m", "temperature_100m", "temperature_200m", "temperature_300m"]

def _get_order_num_of_variable(variables):
    _index_list = []
    for i in variables:
        _index_list.append(full_variables.index(i))
    return _index_list

def _get_gird(gird_shape = (20, 20)):
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
def get_historical_weather_data(location, # (latitude, longitude)
                                variables, # vaiables to be extracted
                                data_range, # date range, eg ("2024-12-19", "2025-01-01")
                                models = "knmi_harmonie_arome_netherlands"
                                ):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    # url =  "https://api.open-meteo.com/v1/forecast"
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


def get_grid_historical_weather_data(grid_list,
                                    variables, # vaiables to be extracted
                                    data_range, # date range, eg ("2024-12-19", "2025-01-01")
                                    models = "knmi_harmonie_arome_netherlands"):
    _collected_dataframes = []
    _count = 0
    for _grid in tqdm(grid_list):
        _dataframe = get_historical_weather_data(_grid, variables, data_range, models)
        _collected_dataframes.append(_dataframe)
        if _count != 0:
            # drop the 'date' column
            _collected_dataframes[-1].drop(columns = 'date', inplace = True)
        _count += 1
    
    return pd.concat(_collected_dataframes, axis = 0)

if __name__ == "__main__":
    # print(_get_gird())
    # data = get_historical_weather_data((49, 0), full_variables[:2], ("2024-03-29", "2024-09-01"))
    collected_data = get_grid_historical_weather_data(_get_gird(), full_variables[:2], ("2024-08-29", "2024-09-01"))