#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) Copyright Bin Cao & Stephan Gruber
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# For variable codes and units of ERA-Interim, see: 
#     http://www.ecmwf.int/publications/manuals/d/gribapi/param/
#
#==============================================================================
#A example of extracting topographic factors, e.g. mrvbf, hypsometirc, from
#fine scale of DEM.
#==============================================================================

######################### HOW TO RUN THIS #####################################
#
# (1) Adapt the script below (settings) and run it
# (2) Make sure the input DEM is larger than required area
#
###############################################################################

from os import path

# =============================== SETTING-UP =================================
dir_scr= 'C:/OneDrive/GitHub/REDCAPP' #toposcale directory
dir_data= 'C:/OneDrive/GitHub/REDCAPP/Data' #Data directory
file_out= 'C:/OneDrive/GitHub//REDCAPP/Result/topo_testArea.nc' #output directory

execfile(path.join(dir_scr, 'topography.py'))

dem = path.join(dir_data, 'DEM_testArea.nc')
demResoultion = 3./3600 #in degree
# ==================================== RUN ===================================
#topographic factors simultions
topo = topography(dem,demResoultion)
topo.describe()#dem description

mrvbf= topo.nmrvbf(out_xy = None, initTf = 50.0)
hypso= topo.coarseHypso(out_xy = None, bound = 30)
eleRange= topo.eleRange(out_xy = None, bound = 30)

#exprot
topoEx = topoExport(mrvbf, hypso, eleRange, demFile = dem)
topoEx.spatialTopo(file_out)