#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 14:56:45 2022

@Author: Eric Chen

@Company: Roivant Sciences

@Email: eric.chen@roivant.com

"""

#######

# diff the GIST energy value from gist.dat

import os

os.chdir("/Users/ericchen/Desktop/matt_diff_gist")

gist_dat_1="/Users/ericchen/Desktop/matt_diff_gist/wee1_apo_gist.dat"

gist_dat_2="/Users/ericchen/Desktop/matt_diff_gist/wee1_lig_gist.dat"


density_cutoff=3
dE_cutoff = 5 # only show the voxel with larget 


def extract_gO_gE(gist_dat):
    
    """
        input: gist_dat, the raw output file from GIST
        
        retrun: a dictionary {"gC":[coordinates],"gO":[water density],"gE":[normalized energy]}
    """
    
    data=open(gist_dat,"r").readlines()
    
    gO=[]
    gE=[]
    gC=[]
    
    for line in data[2:]:
        
        records=line.split()
        
        coordinate=[float(records[1]),float(records[2]),float(records[3])]
        
        density=float(records[22])
        
        energy=float(records[12]) + float(records[14])
        
        gO.append(density)
        gE.append(energy)
        gC.append(coordinate)
    
    return {"gC":gC,"gO":gO,"gE":gE}


def Generate_PDB_gO_gE(coordinate,gO,gE):
    
    """
    
    input: three list of coodinates, water density, normalized water energy
    
    return: generate a pdb file, in which occpancy 
    
     write coordinate, gO, gE into 
    """

dat_1 = extract_gO_gE(gist_dat_1)

dat_2= extract_gO_gE(gist_dat_2)


total_voxel_num= len(dat_1["gO"])


f=open("delta_gist.pdb","w+")

f.write("REMARK                 Site        X       Y       Z     O2-O1    E2-E1     \n")


atom_index = 0

for i in range(total_voxel_num):
    
    delta_gE = dat_2["gE"][i] - dat_1['gE'][i]

    
    if (dat_1["gO"][i] >  density_cutoff or dat_2["gO"][i]> density_cutoff) and abs(delta_gE) > dE_cutoff :
        
        
        
        x=dat_1["gC"][i][0]
        y=dat_1["gC"][i][1]
        z=dat_2["gC"][i][2]
        
        delta_gO = dat_2["gO"][i] - dat_1["gO"][i]
        
        
        pdb_format="%-6s%5s %-4s%1s%3s %1s%4s    %8.3f%8.3f%8.3f%6.1f%6.1f      %-2s%s%s\n"
        
        f.write( pdb_format % ("ATOM",atom_index,"O"," ","WAT","W",atom_index,x,y,z,delta_gO,delta_gE,"","","O"))
        
        atom_index+=1

f.close()
        
        
        
    
    
        
        
        
        
    
    
    