# REanalysis Downscaling Cold Air Pooling Parameterization (REDCAPP )

# What is REDCAPP

REDCAPP is a python-based open source software for parameterizing the temporal and spatial differentiation of surface effects and cold air pooling when downscaling reanalysis data in mountainous areas. REDCAPP can produce daily, high-resolution gridded fields of near-surface air temperature in mountains.
Full desciption available in this publication: http://www.geosci-model-dev-discuss.net/gmd-2017-60/

REDCAPP was originally written with Python 2:  [https://github.com/geocryology/REDCAPP](https://github.com/geocryology/REDCAPP) . This version switch to Python 3.

# Why REDCAPP is Powerful

REDCAPP simulates high-resolution near-surface air temperaure well through providing a number of tools for

(1) downloading and manipulation of ERA-Interim or ERA5 data saved as netCDF4;

(2) contucting the interpoaltion of 2-meter air temperature and pressure level temperatures (or upper-air temperature);

(3) deriving proxy of land-surface effects from reanalysis data;

(4) addressing the spatially varying land-surface effects based on fine-scale DEM;

Additionally, the input data are not limited to ERA-Interim or ERA5, and could be extended to other reanalyses such as CFST, NCEP, MERRA or 20CRV2.

# How to Install

You need to install required dependencies firstly. `conda` is recommended to install those dependencies with one command :

```bash
conda install -c conda-forge netCDF4 pygrib numpy scipy pandas rioxarray xarray dask  -y
```

Then, install REDCAPP to your python site-package (This commend only for Python 3 version):

## Install from GitHub:

```bash
pip install https://github.com/Fanchengyan/REDCAPP.git
```

## Install from local:

download the source code from GitHub:

```bash
git clone https://github.com/Fanchengyan/REDCAPP.git
```

Go to the package directory:

```bash
cd REDCAPP
```
Then, install the package:

```bash
pip install .
```


# How to Run REDCAPP

REDCAPP is wrotten by python (version 2.7 / 3.8 or higher) and public open. To run the software, please

1. Get REDCAPP with :

   - python3: [https://github.com/Fanchengyan/REDCAPP](https://github.com/Fanchengyan/REDCAPP)
2. Register to API:

   1. For ERA-Interim data:
      - Register to ECMWF (free): https://apps.ecmwf.int/registration/
      - Follow the instructions for [Installing your API key](https://confluence.ecmwf.int/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch#AccessingECMWFdataserversinbatch-key)
      - Please accept the terms and conditions at [http://apps.ecmwf.int/datasets/licences/general](http://apps.ecmwf.int/datasets/licences/general)
   2. For ERA5 data
      - Register to CDS (free): <https://cds.climate.copernicus.eu/user/register>
      - Follow the instructions for [How to use the CDS API | (copernicus.eu)](https://cds.climate.copernicus.eu/api-how-to)
      - Please accept the terms and conditions at [Licence to use Copernicus Products](https://cds.climate.copernicus.eu/cdsapp/#!/terms/licence-to-use-copernicus-products)
      
3. Run the script (redcapp_example_ecmwf.py and redcapp_example_era5.py are example scripts)
4. Explore the results. Use a netcdf viewer to plot maps and time series.
   Panoply (https://www.giss.nasa.gov/tools/panoply) is a good one.
5. Customise the code and use it for your project.

# Contact

Please let us know how things work. We hope this is useful for you.

Bin Cao (caobin198912@outlook.com)
