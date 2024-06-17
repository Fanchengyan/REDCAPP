from pathlib import Path
from time import time

import numpy as np

from redcapp import ERA5_Manager, install_CDS_API_key, raster2nc, redcappTemp

# set the directory containing all raw data and output data
home_dir = Path("/Volumes/Data/GeoData/YNG/Temperature")

dem_file = home_dir / "your_dem.tif"

# output dem file in netcdf format
dem_nc = home_dir / "DEM_WGS84.nc"

# output files
spatTopo_out = home_dir / "spatTopo.nc"
spatTemp_out = home_dir / "spatialT.nc"

############# For first time only: install CDS_API_key  ##################

### get your key from https://cds.climate.copernicus.eu/api-how-to
### and replace 'your key' with your key and uncomment the following lines:

install_CDS_API_key(
    url="https://cds.climate.copernicus.eu/api/v2",
    key="your key",
)

############################################################################

######### convert DEM to netcdf format in WGS84 #########

# Note: You can clip DEM by specifying the bbox parameter in WGS84
# bbox = [minx, miny, maxx, maxy]
bbox = None
raster2nc(dem_file, dem_nc, bbox=bbox)

# prepare parameters for downloading data
era5 = ERA5_Manager(home_dir)

pl = era5.get_pressure_levels(min=500, max=1000)
year, month, day, t = era5.generate_datetime("2017", "2023", freq="1D")
area = era5.get_area_from_DEM(dem_nc)
date = era5.get_date_range("2017-01-01", "2023-5-1")


################  Download data  ########################
era5.retrieve_single_levels(year, month, day, t, area)
era5.retrieve_pressure_levels(pl, year, month, day, t, area)


############### Merge and format downloaded data ###################
# Note: merged and formatted data are saved in "data/merge" folder
era5.merge_nc(name="pl")
era5.merge_nc(name="sl")
era5.format_nc(era5.geop)


################# Interpolation Temperature #################
time_s = time()
Redcapp = redcappTemp(era5.get_geop(), era5.get_sa(), era5.get_pl(), date, dem_nc)
Redcapp.extractSpatialDataNCF_TS(spatTopo_out, spatTemp_out)


elapsed_time = time() - time_s
hour = int(elapsed_time / 3600)
minite = int(np.mod((elapsed_time / 60), 60))
sec = int(np.mod(elapsed_time, 60))
print("\nElapsed time: {0:02}h {1:02}m {2:02}s".format(hour, minite, sec))
print("\nElapsed time: {0:02}h {1:02}m {2:02}s".format(hour, minite, sec))
print("\nElapsed time: {0:02}h {1:02}m {2:02}s".format(hour, minite, sec))
