
# KNMI Data Exploration

This repository provides tools to explore and analyze meteorological data obtained from the **KNMI (Royal Netherlands Meteorological Institute)**. It consists of two main scripts:

1. **`download_data_by_api.py`**: Script for downloading KNMI data, after that you need to decompress the file mannually.
2. **`openmeteo_api_connector.py`**: Script for reading and processing the weather data from the API.

---


## Requirements

Ensure the following Python libraries are installed:
- `xarray`
- `cfgrib`
- `eccodes`
- `pygrib` (optional, for detailed GRIB inspections)
- `numpy`
- `pandas`

