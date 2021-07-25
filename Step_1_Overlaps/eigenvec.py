"""Script for generating overlap data for the constituent molecules and the system"""

import numpy as np

def eigen_element (line):
    element = 0
    line_list = line.strip().split()
    if len(line_list) == 5:
        element = line_list[3]
    elif len(line_list) == 3:
        element = line_list[1]
    elif element == 0 or line_list[0] == 'Eigenvector:':
        return None
    return float(element)

def eigen_vector (state, n_lines, all_lines):
    eigen_element_list = []
    for line in all_lines[2+n_lines*state : 2+n_lines*state+n_lines]:
        eigen_element_list.append(eigen_element(line))
    eigen_element_list = [i for i in eigen_element_list if i is not None]
    del eigen_element_list[0]
    eigen_vector = np.array(eigen_element_list)
    return eigen_vector

def all_eigen_vectors (fileobj, natoms_with_p, natoms_with_s, n_states):
    all_lines = fileobj.readlines()
    n_lines = natoms_with_p * 5 + natoms_with_s * 2 + 2
    tmp_list = []
    for state in range(0, n_states):
        tmp_list.append(eigen_vector(state, n_lines, all_lines))
    all_eigen_vectors = np.array(tmp_list)
    fileobj.close()
    return all_eigen_vectors

def create_zeroes (molecule_vec, system_vec, molecule_pos) :
    n_molecule = molecule_vec.shape[1]
    n_system = system_vec.shape[1]
    n_zeroes = n_system - n_molecule
    zero_array = np.zeros((n_molecule,n_zeroes), dtype = float)
    if molecule_pos == "Bottom" :
        molecule_vec_zeroes = np.concatenate((zero_array, molecule_vec), axis = 1)
    elif molecule_pos == "Top" :
        molecule_vec_zeroes = np.concatenate((molecule_vec, zero_array), axis=1)
    return molecule_vec_zeroes

def normalise (vec) :
    norm = np.linalg.norm(vec)
    normal_array = vec/norm
    return normal_array

#The conditional statements and string values of this function can be changed as per our needs
def overlap (molecule_vec, system_vec) :
    f_ov = open("overlap.txt", "w")
    tmp_list_molecule = molecule_vec.tolist()
    tmp_list_system = system_vec.tolist()
    for i in molecule_vec :
        for j in system_vec :
            overlap = np.dot(normalise(i), normalise(j))
            if overlap >= 0.2:
                txt = "2H2PC : {} Charge_System : {} Overlap : {} \n"
                tmp_list_i = i.tolist()
                arg1 = tmp_list_molecule.index(tmp_list_i)
                tmp_list_j = j.tolist()
                arg2 = tmp_list_system.index(tmp_list_j)
                if arg2 not in range(306, 312) :
                    break
                f_ov.write(txt.format(arg1,arg2,overlap))
    f_ov.close()
    return

f_bucky_sys = open("charge_system_eigen.txt", "r")
f_2H2PC = open("2H2PC_eigen.txt", "r")
f_bucky = open("bucky_eigen.txt", "r")

H2PC_vec = all_eigen_vectors(f_2H2PC, 80, 36, 356)
bucky_sys_eigen_vec = all_eigen_vectors(f_bucky_sys, 140, 36, 596)
bucky_eigen_vec = all_eigen_vectors(f_bucky, 60, 0, 240)
H2PC_with_zeroes = create_zeroes(H2PC_vec, bucky_sys_eigen_vec, "Top")
bucky_with_zeroes = create_zeroes(bucky_eigen_vec, bucky_sys_eigen_vec, "Bottom")
overlap(H2PC_with_zeroes, bucky_sys_eigen_vec)
#overlap(bucky_with_zeroes, bucky_sys_eigen_vec)


























