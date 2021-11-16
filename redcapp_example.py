# -*- coding: utf-8 -*-
#
# REanalysis Downscaling Cold Air Pooling Parameterization (REDCAPP)
#
# === COPYRIGHT AND LICENCE ====================================================
#
# Copyright 2017 Bin Cao & Stephan Gruber
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ==============================================================================
#
# Example file containing: (a) data download,
#                          (b) obtaining spatialized mean air temperature
#                          (c) obtaining air temperature time series at point
#
# (1) Get REDCAPP at https://github.com/geocryology/REDCAPP
#
# (2) Make sure that the directory containing thie file (redcapp_example.py) is
#     contained in your PYTHONPATH.
#
# (3) Register to ECMWF (free) https://apps.ecmwf.int/registration/
#
# (4) Follow the instructions for "Installing your API key" on
# https://software.ecmwf.int/wiki/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch
#
# (5) Adapt the script below (settings and location)
#
# (6) Run the script
#
# (7) Explore the results. Use a netcdf viewer to plot maps and time series.
#     Panoply (https://www.giss.nasa.gov/tools/panoply) is a good one.
#
# (8) Customise the code and use it for your project.
#
# (9) Please let us know how things work. We hope this is useful for you.
#
# ==============================================================================
# %%
import os
from redcapp import redcapp_get, eraData, DataManager, redcappTemp
from datetime import datetime
from pathlib import Path
from time import time
import numpy as np
# directory containing all raw data and output data
dir_data = Path('/media/fanchy/data/GeoData/temp/data')

# input Digital ELevation Model in ASCIIGRID format and lat/lon WGS84 grid,
# must be (a) in directory indicated above, (b) situated within area indicated
# below, and (c) encompass the station locations given below.
dem_in = 'DEM.asc'

# output file names
spatTopo_out = 'spatTopo.nc'  # modeled spatialized geomorphometric factors
statTopo_out = 'statTopo.csv'  # modeled spatation geomorphometric factors
spatTemp_out = 'spatialT.nc'  # spatialised mean air temperature
statTemp_out = 'stationT.csv'  # station timeseries air temperature
dem_ncdf = 'DEM.nc'

#location: alps
date = {'beg': datetime(2015, 12, 1, 00, 00),
        'end': datetime(2015, 12, 1, 00, 00)}

area = {'north': 48,
        'south': 45.55,
        'west': 8.90,  # positive is westwards of Greenwich
        'east': 11.3}  # positive is westwards of Greenwich

elevation = {'min': 0,
             'max': 4500}

# Format of stations for which to provide time series
# ['name':'siteName','lat':latNumber, 'lon':lonNumber, 'ele':eleNumber]
stations = [{'name': 'COV', 'lat': 46.41801198, 'lon': 9.821232448, 'ele': 3350.5},
            {'name': 'SAM', 'lat': 46.52639523, 'lon': 9.878944266, 'ele': 1756.2}]

# make full file names
dem_ascii = dir_data / dem_in
dem_ncdf = dir_data / dem_ncdf
spatTopo_out = dir_data / spatTopo_out
statTopo_out = dir_data / statTopo_out
spatTemp_out = dir_data / spatTemp_out
statTemp_out = dir_data / statTemp_out

# dem resolution
# resolution = 3.0/3600
# %%
# === DOWNLOAD =================================================================
# rg = redcapp_get(date, area, elevation, dir_data, 5)
# rg.retrieve()

# eraDownload = eraData()
# eraDownload.NCDFmergeWildcard(path.join(dir_data, 'ecmwf_erai_sa_*'), 1)
# eraDownload.NCDFmergeWildcard(path.join(dir_data, 'ecmwf_erai_pl_*'), 1)

# %%
# ==== IMPORT REANALYSIS =======================================================
dm = DataManager(dir_data)
sa = dm.saf_get()    # 2-meter air temperature
pl = dm.plf_get()    # pressure level air temperature
geop = dm.geopf_get()  # geopotential file

# %%
# ==== DEM CONVERSION ==========================================================
# convert ASCII DEM to netcdf format.
if os.path.exists(dem_ncdf):
    os.remove(dem_ncdf)
dm.raster2nc(dem_ascii, dem_ncdf)

# ==== REDCAPP TEMPERATURE =====================================================
# setting-up
time_s = time()
variable = 'Temperature'
Redcapp = redcappTemp(geop, sa, pl, variable, date, dem_ncdf, resolution)

# SPATIALIZED MEAN AIR TEMPERATURE
Redcapp.extractSpatialDataNCF(spatTopo_out, spatTemp_out)

# STATION AIR TEMPERATURE TIME SERIES
Redcapp.extractStationDataCSV(stations, statTopo_out, statTemp_out)

elapsed_time = time()-time_s
hour = int(elapsed_time/3600)
minite = int(np.mod((elapsed_time/60), 60))
sec = int(np.mod(elapsed_time, 60))
print("\nElapsed time: {0:02}h {1:02}m {2:02}s".format(hour, minite, sec))
# %%
