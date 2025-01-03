import cfgrib
import matplotlib.pyplot as plt


# File path to your GRIB file
file_path = r'HARM43_V1_P1_2025010210\HA43_N20_202501021000_00900_GB'


datasets = cfgrib.open_datasets(file_path)
ds = datasets[1]  # For example, Dataset 1

ds_var_value = ds.data_vars['unknown']

print(ds_var_value.values.shape)

# Plot the data
ds_var_value[9].plot()
# two_d_data = ds_var_value.isel(heightAboveGround=0)
# two_d_data.plot()
plt.title("Unknown Data Variable")
plt.show()

_latitude = ds_var_value.latitude.values
_longitude = ds_var_value.longitude.values
_grid = dict(latitude=_latitude, longitude=_longitude)
print(_grid)

# save the grid as a pickle file
import pickle

with open('grid.pkl', 'wb') as f:
    pickle.dump(_grid, f)
