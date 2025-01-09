import xarray as xr
import cfgrib

file_path = r'HARM43_V1_P1_2024121611\HA43_N20_202412161100_00500_GB'

# Possible filter keys to explore
filters = [
    {'typeOfLevel': 'heightAboveGround', 'stepType': 'instant'},
    {'typeOfLevel': 'heightAboveGround', 'stepType': 'accum'},
    # {'typeOfLevel': 'heightAboveSea'},
    # {'typeOfLevel': 'entireAtmosphere'}
]

# Dictionary to store the datasets
datasets = {}

# Attempt to read the file with each filter
for filter_by_keys in filters:
    try:
        print(f"Trying with filter: {filter_by_keys}")
        ds = xr.open_dataset(file_path, engine='cfgrib', filter_by_keys=filter_by_keys)
        datasets[str(filter_by_keys)] = ds  # Store the dataset with its filter as the key
        print(f"Loaded dataset with filter {filter_by_keys}")
        print(ds)  # Metadata for inspection
    except Exception as e:
        print(f"Error with filter {filter_by_keys}: {e}")

# List all datasets and variables
if datasets:
    print("\nAll loaded datasets and variables:")
    for key, ds in datasets.items():
        print(f"\nFilter: {key}")
        print("Variables:")
        for var_name in ds.variables:
            print(f"  - {var_name}")
        # Close the dataset
        ds.close()
else:
    print("No datasets could be loaded.")
