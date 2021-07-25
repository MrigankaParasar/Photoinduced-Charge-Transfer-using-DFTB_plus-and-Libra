'''Script to generate the time dependent eigenvalues
    of the system over the MD trajectory '''

import os

md_file = open("md.xyz", "r")
lines_md_file = md_file.readlines()
time = 0
for i in range(0, 35778, 178) :
    geom_file = open("charge_system.xyz", "w")
    for j in range(i, i+178):
        geom_file.write(lines_md_file[j])
    geom_file.close()
    os.system("dftb+")
    eigenvalue_file = open("band.out", "r")
    os.system("mv band.out Time_Step_%s.txt" % str(time))
    eigenvalue_file.close()
    os.system("rm charge_system.xyz")
    time += 1













