#***********************************************************
# * Copyright (C) 2020 Brendan A. Smith and Alexey V. Akimov
# * This file is distributed under the terms of the
# * GNU General Public License as published by the
# * Free Software Foundation; either version 3 of the
# * License, or (at your option) any later version.
# * http://www.gnu.org/copyleft/gpl.txt
#***********************************************************/

from liblibra_core import *
from libra_py import *
import sys
import os
import numpy as np

# This file runs the thermal sampling from a MD trajectory

cwd = os.getcwd()

natoms = 176
# set number of sub-trajs
nsub   = 10

rnd = Random()
# Store random numbers
traj_id = []
traj_list = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
# Select nsub points along given MD traj
for i in range(nsub):
    traj_id.append(traj_list[i])

dirname = "traj"

print( "traj_id = " )
print( traj_id )

f = open("md.xyz")
A = f.readlines()
sz = len(A)
f.close()

# get atom IDs
at_iD = []
for i in range(sz):
    b = A[i].strip().split()
    if b[0] == "MD":
        if b[2] == str(0):
            for k in range(natoms):
                bb = A[i+k+1].strip().split()
                at_iD.append(bb[0])

for i in range(nsub):

    # Make new folder for sub-trajectory
    os.system("mkdir %s" % (dirname+str(i)) )
 
    # Move needed files to folder 
    os.system("cp dftb_in.hsd %s" % (dirname+str(i)) )
    os.system("cp md.xyz %s" % (dirname+str(i)) )
    os.system("cp bucky&benzene.gen %s" % (dirname + str(i)))

    # Get the positions and velocities for random traj_id
    vel = MATRIX(3*natoms,1)
    pos = MATRIX(3*natoms,1)
    for j in range(sz):
        b = A[j].strip().split()  
        if b[0] == "MD":                  
            if b[2] == str(traj_id[i]):
                #print str(traj_id[i])
                for k in range(natoms):
                    bb = A[j+k+1].strip().split()

                    pos.set(3*k,0,float(bb[1]))
                    pos.set(3*k+1,0,float(bb[2]))
                    pos.set(3*k+2,0,float(bb[3]))

                    vel.set(3*k,0,float(bb[5]))
                    vel.set(3*k+1,0,float(bb[6]))
                    vel.set(3*k+2,0,float(bb[7]))

    # Now write these to and xyz and txt file, respectively
    _pos = open("position.xyz","w")
    _pos.write("  %i\n\n" % (natoms) )

    _vel = open("velocity.txt","w")

    for j in range(natoms):
        _pos.write("%s %8.5f  %8.5f  %8.5f\n" % (at_iD[j], pos.get(3*j), pos.get(3*j+1), pos.get(3*j+2) ) )
        _vel.write("%8.5f  %8.5f  %8.5f\n" % (vel.get(3*j), vel.get(3*j+1), vel.get(3*j+2) ) )
    _pos.close()
    _vel.close()

    # Convert position.xyz to position.get
    os.system("python convert.py")

    # Move the files into that directory
    os.system("cp position.gen %s" % (dirname+str(i)) )
    os.system("cp velocity.txt %s" % (dirname+str(i)) )

    # Run the dftb+ input files for sub-trajectory
    os.chdir((dirname+str(i)))
    os.system("dftb+")
    os.chdir(cwd)

