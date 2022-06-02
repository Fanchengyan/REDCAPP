from redcapp import data_manager as dm
from redcapp import redcappTemp, raster2nc
from pathlib import Path
from time import time
import numpy as np

dem_file = '/media/fanchy/Seagate/LicSAR_QTP/descending/106D_05049_131313/temperature/era5/result/DEM_cliped.tif'


folder = Path(
    '/media/fanchy/Seagate/LicSAR_QTP/descending/106D_05049_131313/temperature/era5')
dem_nc = '/media/fanchy/Seagate/LicSAR_QTP/descending/106D_05049_131313/temperature/era5/result/DEM_cliped.nc'

spatTopo_out = folder / 'result/spatTopo.nc'
spatTemp_out = folder / 'result//spatialT.nc'


############# For first time only: install CDS_API_key  ##################
# dm.install_CDS_API_key(url='https://cds.climate.copernicus.eu/api/v2',
#                        key='your key')

raster2nc(dem_file, dem_nc)


era5 = dm.ERA5_Manager(folder)

pl = era5.get_pressure_levels(min=500, max=1000)
year, month, day, t = era5.generate_datetime('2014', '2021', freq='1D')
area = era5.get_area_from_DEM(dem_file)
date = era5.get_date_range('2014-01-01', '2021-12-31')

################  download data  ########################
era5.retrieve_single_levels(year, month, day, t, area)
era5.retrieve_pressure_levels(pl, year, month, day, t, area)


############### merge and format data ###################
pl = era5.merge_nc(
    name='pl',
    merged_file=None,
    day_mean=True,
    format=True
)

sa = era5.merge_nc(
    name='sl',
    merged_file=None,
    day_mean=True,
    format=True
)

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


elapsed_time = time()-time_s
hour = int(elapsed_time/3600)
minite = int(np.mod((elapsed_time/60), 60))
sec = int(np.mod(elapsed_time, 60))
print("\nElapsed time: {0:02}h {1:02}m {2:02}s".format(hour, minite, sec))
