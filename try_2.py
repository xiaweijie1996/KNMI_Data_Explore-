import cfgrib
import matplotlib.pyplot as plt


# File path to your GRIB file
file_path = r'HARM43_V1_P1_2024121611\HA43_N20_202412161100_00900_GB'


datasets = cfgrib.open_datasets(file_path)
ds = datasets[3]  # For example, Dataset 1

ds_var_value = ds.data_vars['unknown']

print(ds_var_value.values.shape)

# Plot the data
ds_var_value.plot()
# two_d_data = ds_var_value.isel(heightAboveGround=0)
# two_d_data.plot()
plt.title("Unknown Data Variable")
plt.show()