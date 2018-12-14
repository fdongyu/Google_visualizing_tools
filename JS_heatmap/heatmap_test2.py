# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:29:16 2018

@author: dongyu
"""

import numpy as np
from netCDF4 import Dataset, num2date
import utm

from Pmap_Google_earth import GoogleMapHeatmap

import pdb


def read_GNOME(infile):
    """
    read GNOME
    """        
            
    nc = Dataset(infile,'r')
    t = nc.variables['time']
    time = num2date(t[:],t.units)
    
    tlen=len(nc.variables['time'])
    td=len(nc.variables['spill_num'])
    nn=td/tlen
    
    lat = nc.variables[u'latitude'][:]
    lon = nc.variables[u'longitude'][:]
    
    lat_new = np.zeros([tlen, nn])        
    lon_new = np.zeros([tlen, nn])
    for ii in range(tlen):
        lat_new[ii,:] = lat[ii*nn:(ii+1)*nn]
        lon_new[ii,:] = lon[ii*nn:(ii+1)*nn]

    return time, lat_new, lon_new        
#    xp0 = np.zeros([tlen,nn])
#    yp0 = np.zeros([tlen,nn])
#    for ii in range(tlen):
#        for jj in range(nn):
#            xp0[ii,jj], yp0[ii,jj] = utm.from_latlon(lat_new[ii,jj], lon_new[ii,jj])[0:2]
                    
#    return time, xp0, yp0



caseID = 'case21'
basedir = '../%s/multi_tracks/fine'%caseID
basedir_coarse = '../%s/multi_tracks/coarse'%caseID

filename_coarse = '../example_case2/backups/%s/multi_tracks/coarse/0/GNOME_output.nc'%caseID
filename_fine = '../example_case2/backups/%s/multi_tracks/fine/0/GNOME_output.nc'%caseID

hoursSince = [10,20,30,40,50]
files = []
files_coarse = []
for hours in hoursSince:
    files.append('%s/%s/GNOME_output.nc'%(basedir, str(hours)))
    files_coarse.append('%s/%s/GNOME_output.nc'%(basedir_coarse, str(hours)))

tp1, lat1, lon1 = read_GNOME(filename_coarse)
tp2, lat2, lon2 = read_GNOME(filename_fine)

pdb.set_trace()

truncate_time = 220   

lat1 = lat1[:truncate_time]
lon1 = lon1[:truncate_time]
lat2 = lat2[:truncate_time]
lon2 = lon2[:truncate_time]

 
lat0 = []
lon0 = []

lat0.append(np.ravel(lat1))
lat0.append(np.ravel(lat2))
lon0.append(np.ravel(lon1))
lon0.append(np.ravel(lon2))


for i in range(4)[::-1]:
    filename = files[i]
    tp11, lat11, lon11 = read_GNOME(filename)
    
    filename2 = files_coarse[i]
    tp22, lat22, lon22 = read_GNOME(filename2)    
    
    lat_new = np.concatenate((lat11, lat22), axis=0) 
    lon_new = np.concatenate((lon11, lon22), axis=0)
    lat_new = lat_new[:truncate_time]
    lon_new = lon_new[:truncate_time]
    
    lat_tem = np.ravel(lat_new)
    lon_tem = np.ravel(lon_new)
    lat0.append(lat_tem)
    lon0.append(lon_tem)

lat = np.hstack(lat0)
lon = np.hstack(lon0)

GMH = GoogleMapHeatmap(29.529934, -94.831831, 12)
GMH.heatmap(lat, lon, maxIntensity=0.2)
GMH.draw('heat2.html')
pdb.set_trace()








