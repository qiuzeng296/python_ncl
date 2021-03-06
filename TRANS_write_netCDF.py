#
#  File:
#    TRANS_write_netCDF.py
#
#  Synopsis:
#    Illustrates how to write a netCDF file
#
#  Categories:
#    I/O
#
#  Author:
#    Karin Meier-Fleischer, based on NCL example
#  
#  Date of initial publication:
#    September 2018
#
#  Description:
#    This example shows how to write a netCDF file.
#
#  Effects illustrated:
#    o  Reading netCDF file
#    o  Converting data from Kelvin to degC
#    o  Writing data to new netCDF file
#    o  Detailed version
#
#  Output:
#    netCDF data file.
#
#  Notes: The data for this example can be downloaded from 
#    http://www.ncl.ucar.edu/Document/Manuals/NCL_User_Guide/Data/
#   
"""
  Transition Guide Python Example:   TRANS_write_netCDF.py

  -  Reading netCDF file
  -  Converting data from Kelvin to degC
  -  Writing data to new netCDF file
  -  Detailed version

  2018-08-28  kmf
"""
import os
import numpy as np
import Ngl,Nio

#--  data file name
fname  = "rectilinear_grid_3D.nc"

#-- open file
f = Nio.open_file(fname, "r")

#-- read temperature, time, latitude and longitude arrays
var  = f.variables["t"]
time = f.variables["time"]
lat  = f.variables["lat"]
lon  = f.variables["lon"]

#-- convert data from units Kelvin to degC
varC =  var[:,0,:,:]                       #-- copy variable at level=0; retain metadata
varC =  varC-273.15                        #-- convert to degC

#-- open new netCDF file
os.system("rm -rf t_degC_py.nc")           #-- delete file if it exists
outf = Nio.open_file("t_degC_py.nc","c")   #-- open new netCDF file

#-- create dimensions
outf.create_dimension('time',None)
outf.create_dimension('lat',f.dimensions['lat'])
outf.create_dimension('lon',f.dimensions['lon'])

#-- create dimension variables
outf.create_variable('time',time.typecode(),time.dimensions)
varAtts = list(time.__dict__.keys())
varAtts.sort()
for att in varAtts:
	value = getattr(time,att)                   #-- get attributes
	setattr(outf.variables['time'],att,value)   #-- copy attributes

outf.create_variable('lat',lat.typecode(),lat.dimensions)
varAtts = list(lat.__dict__.keys())
varAtts.sort()
for att in varAtts:
	value = getattr(lat,att)                    #-- get attributes
	setattr(outf.variables['lat'],att,value)    #-- copy attributes

outf.create_variable('lon',lon.typecode(),lon.dimensions)
varAtts = list(lon.__dict__.keys())
varAtts.sort()
for att in varAtts:
	value = getattr(lon,att)                    #-- get attributes
	setattr(outf.variables['lon'],att,value)    #-- copy attributes

#-- create variable
outf.create_variable('t','f',('time','lat','lon'))
setattr(outf.variables['t'], 'standard_name', 'temperature')
setattr(outf.variables['t'], 'units', 'degC')

#-- assign values --> write data to file
outf.variables['time'].assign_value(time)
outf.variables['lat'].assign_value(lat)
outf.variables['lon'].assign_value(lon)
outf.variables['t'].assign_value(varC)

#-- close output stream (not necessary)
outf.close()
