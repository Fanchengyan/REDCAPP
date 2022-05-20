# REanalysis Downscaling Cold Air Pooling Parameterization (REDCAPP )

# What is REDCAPP
REDCAPP is a python-based open source software for parameterizing the temporal and spatial differentiation of surface effects and cold air pooling when downscaling reanalysis data in mountainous areas. REDCAPP can produce daily, high-resolution gridded fields of near-surface air temperature in mountains.
Full desciption available in this publication: http://www.geosci-model-dev-discuss.net/gmd-2017-60/

REDCAPP was originally written with Python 2:  <https://github.com/geocryology/REDCAPP> . This version switch to Python 3.


# Why REDCAPP is Powerful 
REDCAPP simulates high-resolution near-surface air temperaure well through providing a number of tools for

(1) downloading and manipulation of ERA-Interim data saved as netCDF4;

(2) contucting the interpoaltion of 2-meter air temperature and pressure level temperatures (or upper-air temperature);

(3) deriving proxy of land-surface effects from reanalysis data;

(4) addressing the spatially varying land-surface effects based on fine-scale DEM;


Additionally, the input data are not limited to ERA-Interim and could be extended to other reanalyses such as CFST, NCEP, MERRA or 20CRV2.

# How to Install

You need to install required dependencies firstly. `conda` is recommended to install those dependencies with one command :

```bash
conda install -c conda-forge netCDF4 pygrib numpy scipy rioxarray xarray -y
```

Install `ecmwfapi` using pip:

```bash
pip install ecmwf-api-client
```

Then, install REDCAPP to your python site-package (This commend only for Python 3 version):

```bash
python setup.py install
```

# How to Run REDCAPP
REDCAPP is wrotten by python (version 2.7 / 3.6 or higher) and public open. To run the software, please

(1) Get REDCAPP with :

- python2: <https://github.com/geocryology/REDCAPP>  
- python3: <https://github.com/Fanchengyan/REDCAPP>

(2) Register to ECMWF (free) https://apps.ecmwf.int/registration/

(3) Follow the instructions for "Installing your API key" on
    https://software.ecmwf.int/wiki/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch

(4)  Please accept the terms and conditions at <http://apps.ecmwf.int/datasets/licences/general>

(5) Run the script (redcapp_example.py is an example script)

(6) Explore the results. Use a netcdf viewer to plot maps and time series.
    Panoply (https://www.giss.nasa.gov/tools/panoply) is a good one.

(7) Customise the code and use it for your project.



# Contact
Please let us know how things work. We hope this is useful for you.

Bin Cao (caobin198912@outlook.com)
