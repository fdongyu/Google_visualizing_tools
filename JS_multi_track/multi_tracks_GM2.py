# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:29:16 2018

@author: dongyu
"""

import numpy as np
from netCDF4 import Dataset, num2date
import utm

import gmplot_new 

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

truncate_time = 220    

lat1 = lat1[:truncate_time]
lon1 = lon1[:truncate_time]
lat2 = lat2[:truncate_time]
lon2 = lon2[:truncate_time]

latm1, lonm1 = np.average(lat1, axis=1), np.average(lon1, axis=1)
latm2, lonm2 = np.average(lat2, axis=1), np.average(lon2, axis=1)

## initiate the plot object
gmap = gmplot_new.GoogleMapPlotter(29.529934, -94.831831, 12)

gmap.plot(latm1, lonm1, 'cornflowerblue', edge_width=3, name='coarse-grid')
gmap.plot(latm2, lonm2, 'r', edge_width=3, name='fine-grid')
gmap.scatter(lat1[-1,:], lon1[-1,:], 'cornflowerblue', size=120, marker=False)
gmap.scatter(lat2[-1,:], lon2[-1,:], 'r', size=120, marker=False)

colors = ['y', 'k', 'g', 'c', 'm']
names = ['20% fine-grid', '40% fine-grid', '60% fine-grid', '80% fine-grid']
edge_widths = [5, 7, 9, 11]
#for i in range(len(files))[::-1]:
for i in range(4)[::-1]:
    filename = files[i]
    tp11, lat11, lon11 = read_GNOME(filename)
    
    #lat11 = lat11[:truncate_time]
    #lon11 = lon11[:truncate_time]
    #latm11, lonm11 = np.average(lat11, axis=1), np.average(lon11, axis=1)
    
    #### plot coarse files tracks
    filename2 = files_coarse[i]
    tp22, lat22, lon22 = read_GNOME(filename2)

    lat_new = np.concatenate((lat11, lat22), axis=0) 
    lon_new = np.concatenate((lon11, lon22), axis=0)
    lat_new = lat_new[:truncate_time]
    lon_new = lon_new[:truncate_time]

    latm_new, lonm_new = np.average(lat_new, axis=1), np.average(lon_new, axis=1)
    #latm22, lonm22 = np.average(lat22, axis=1), np.average(lon22, axis=1)
    #pdb.set_trace()
    gmap.plot(latm_new, lonm_new, colors[i], edge_width=edge_widths[i], name=names[i])
    #gmap.plot(latm22, lonm22, colors[i], edge_width=8)
    gmap.scatter(lat_new[-1,:], lon_new[-1,:], colors[i], size=120, marker=False)

gmap.marker(latm1[0], lonm1[0], 'r')    
gmap.draw("tracks_multi2.html")
