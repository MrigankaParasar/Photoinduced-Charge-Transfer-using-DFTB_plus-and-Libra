'''
Script to print out the possible transitions over the MD trajectory.
Used for choosing the initial single electron excited state
'''

#Use the overlap output files
acceptor_overlap = open("C60_UMO_overlap.txt", "r")
acceptor_overlap_lines = acceptor_overlap.readlines()
donor_overlap = open("2H2PC_LUMO_overlap.txt", "r")
donor_overlap_lines = donor_overlap.readlines()

donor_lumo = []
acceptor_umo = []

for line in acceptor_overlap_lines :
    line_list = line.strip().split()
    if line_list[5] not in acceptor_umo :
        acceptor_umo.append(int(line_list[5]))

acceptor_umo = sorted(set([x for x in acceptor_umo if x >= 306]))

for line in donor_overlap_lines :
    line_list = line.strip().split()
    if line_list[5] not in donor_lumo :
        donor_lumo.append(int(line_list[5]))

donor_lumo = sorted(set([x for x in donor_lumo if x >= 306]))

acceptor_overlap.close()
donor_overlap.close()

def donor_lumo_energies(file_obj) :
    lines = file_obj.readlines()
    donor_energies = []
    for line in lines[307 : 597] :
        line_list = line.strip().split()
        donor_energies.append(float(line_list[1]))
    donor_lumo_with_energies = list(zip(donor_lumo, donor_energies))
    return donor_lumo_with_energies

def acceptor_umo_energies(file_obj) :
    lines = file_obj.readlines()
    acceptor_umo_energies = []
    for j in range(307, 597):
        line_list = lines[j].strip().split()
        if int(line_list[0]) - 1 in acceptor_umo:
            acceptor_umo_energies.append(float(line_list[1]))
    acceptor_umo_with_energies = list(zip(acceptor_umo, acceptor_umo_energies))
    return acceptor_umo_with_energies


output = open("Possibilities.txt", "w")

for k in range(0, 201) :
    file_obj1 = open("Time_Step_%s.txt" % str(k), "r")
    donor_lumo_with_energies = donor_lumo_energies(file_obj1)
    file_obj1.close()
    file_obj2 = open("Time_Step_%s.txt" % str(k), "r")
    acceptor_umo_with_energies = acceptor_umo_energies(file_obj2)
    file_obj2.close()
    for i in acceptor_umo_with_energies :
        for j in donor_lumo_with_energies :
            if j[0] > i[0] and abs(j[1] - i[1]) < 0.2 :
                text = "Transition from State {} to State {} at {} fs \n"
                output.write(text.format(j[0], i[0], str(k)))

output.close()

file_obj = open("Possibilities.txt", "r")

file_lines = file_obj.readlines()

initial_states = []

for line in file_lines :
    line_list = line.strip().split()
    initial_states.append(int(line_list[3]))

initial_states = list(set(initial_states))
print(initial_states)

file_obj.close()




