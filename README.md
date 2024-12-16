# KNMI_Data_Explore

# KNMI Data Exploration

This repository provides tools to explore and analyze meteorological data obtained from the **KNMI (Royal Netherlands Meteorological Institute)**. It consists of two main scripts:

1. **`access_data_exp.py`**: Script for downloading KNMI data.
2. **`read_data_exp.py`**: Script for reading and processing the downloaded GRIB data.

---

## Features
- **Download Meteorological Data**: Automate the process of fetching data from KNMI servers or other sources.
- **Read and Process GRIB Files**: Extract key information and metadata from GRIB1/GRIB2 files using libraries like `cfgrib` and `eccodes`.
- **Flexible Filtering**: Supports dynamic filtering of GRIB data to extract specific layers (e.g., temperature, pressure, wind speed).

---

## Requirements

Ensure the following Python libraries are installed:
- `xarray`
- `cfgrib`
- `eccodes`
- `pygrib` (optional, for detailed GRIB inspections)
- `numpy`
- `pandas`

