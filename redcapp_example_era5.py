from pathlib import Path
from time import time

import numpy as np

from redcapp import data_manager as dm
from redcapp import raster2nc, redcappTemp

# set the directory containing all raw data and output data
dir_data = Path("/Volumes/Data/GeoData/YNG/Temperature")

folder_out = dir_data / "result"
if not folder_out.is_dir():
    folder_out.mkdir(parents=True)


dem_file = dir_data / "your_dem.tif"

# output dem file in netcdf format
dem_nc = dir_data / "DEM_WGS84.nc"

spatTopo_out = folder_out / "result/spatTopo.nc"
spatTemp_out = folder_out / "result//spatialT.nc"


############# For first time only: install CDS_API_key  ##################

### get your key from https://cds.climate.copernicus.eu/api-how-to
### and replace 'your key' with your key and uncomment the following lines:

# dm.install_CDS_API_key(
#     url="https://cds.climate.copernicus.eu/api/v2",
#     key="your key",
# )

############# For first time only: install CDS_API_key  ##################

# convert DEM to netcdf format in WGS84
raster2nc(dem_file, dem_nc)


era5 = dm.ERA5_Manager(folder_out)

pl = era5.get_pressure_levels(min=500, max=1000)
year, month, day, t = era5.generate_datetime("2017", "2023", freq="1D")
area = era5.get_area_from_DEM(dem_nc)
date = era5.get_date_range("2017-01-01", "2023-5-1")

################  download data  ########################
era5.retrieve_single_levels(year, month, day, t, area)
era5.retrieve_pressure_levels(pl, year, month, day, t, area)


############### merge and format data ###################
pl = era5.merge_nc(name="pl", merged_file=None, day_mean=True, format=True)

sa = era5.merge_nc(name="sl", merged_file=None, day_mean=True, format=True)

geop = era5.format_nc(era5.geop)

###############
pl = era5.get_pl()
sa = era5.get_sa()
geop = era5.get_geop()

#################
time_s = time()
Redcapp = redcappTemp(geop, sa, pl, date, dem_nc)

# SPATIALIZED MEAN AIR TEMPERATURE
Redcapp.extractSpatialDataNCF_TS(spatTopo_out, spatTemp_out)


elapsed_time = time() - time_s
hour = int(elapsed_time / 3600)
minite = int(np.mod((elapsed_time / 60), 60))
sec = int(np.mod(elapsed_time, 60))
print("\nElapsed time: {0:02}h {1:02}m {2:02}s".format(hour, minite, sec))
print("\nElapsed time: {0:02}h {1:02}m {2:02}s".format(hour, minite, sec))
print("\nElapsed time: {0:02}h {1:02}m {2:02}s".format(hour, minite, sec))
