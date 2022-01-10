#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 10:50:07 2022

@Author: Eric Chen

@Company: Roivant Sciences

@Email: eric.chen@roivant.com

"""

## Many useful functions to process GIST data

from gridData import Grid
import numpy as np
import os

# Change the work dir to where the "gist.dat" locates

#os.chdir("/Users/ericchen/Desktop/matt_diff_gist/wee1_apo")



def Generate_dx(dat):
    """
    

    Parameters
    ----------
    dat : gist.dat file from GPU-GIST
        

    Returns
    -------
    dx files for the water property in gist.dat

    """
    
    data=open(dat).readlines()
    
    ### In the gist.dat file, the voxel coordinate is the voxel_center shift by (0.25,0.25,0.25)
    
    x_range=np.arange(float(data[2].split()[1])-0.5,float(data[-1].split()[1])+0.5,0.5)
    y_range=np.arange(float(data[2].split()[2])-0.5,float(data[-1].split()[2])+0.5,0.5)
    z_range=np.arange(float(data[2].split()[3])-0.5,float(data[-1].split()[3])+0.5,0.5)
    
    grid_coordiates=[x_range,y_range,z_range]
    
    x_voxel_num=len(x_range)-1
    y_voxel_num=len(y_range)-1
    z_voxel_num=len(z_range)-1
    
    position_index = []
    
    for x in range(x_voxel_num):
        for y in range(y_voxel_num):
            for z in range(z_voxel_num):
                position_index.append((x,y,z))
    
    # extract the normalized gO, gE(Esw+Eww),gTsix from the output
    
    grid_dimension=(x_voxel_num,y_voxel_num,z_voxel_num)
    
    
    gO=np.zeros(grid_dimension)
    
    E_total_norm=np.zeros(grid_dimension)
    
    TSsix_norm=np.zeros(grid_dimension)
    
    
    voxel=0
    
    for line in data[2:]:
        
        temp=line.split()
        
        gO_temp=float(temp[22])
        
        E_total_temp=0.5*float(temp[12]) + float(temp[14])
        
        TSsix_total_temp=float(temp[10])
        
        gO[position_index[voxel]] = gO_temp
        
        E_total_norm[position_index[voxel]] = E_total_temp
        
        TSsix_norm[position_index[voxel]] = TSsix_total_temp
        
        voxel+=1
    
    Grid(grid=gO,edges=grid_coordiates).export("gO.dx")
    Grid(grid=E_total_norm,edges=grid_coordiates).export("E_total_norm.dx")
    Grid(grid=TSsix_norm,edges=grid_coordiates).export("dTSsix_norm.dx")
    
    
    
Generate_dx("gist.dat")



    
    
    