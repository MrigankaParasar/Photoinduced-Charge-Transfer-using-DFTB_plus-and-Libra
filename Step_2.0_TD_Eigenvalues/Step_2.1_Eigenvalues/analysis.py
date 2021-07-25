'''Script for generating the time dependent eigenspectrum of the LUMOs of interest
    using the output for the previous step'''

lumo = {1 : [],2 : [],3 : [],4 : [],5 : [],6 : [],7 : [],8 : [],9 : [],10 : []}
for i in range(0, 201) :
    file_obj = open("Time_Step_%s.txt" % str(i))
    lines = file_obj.readlines()
    for j in range(317, 327) :
        line_items = lines[j].strip().split()
        for key in lumo.keys() :
            if (int(line_items[0])-316) == key :
                lumo[key].append(float(line_items[1]))


output = open("output.txt", "w")
for i in range(0, 201) :
    output.write("{} {} {} {} {} {} {} {} {} {} {} \n".format(i,lumo[1][i],lumo[2][i],lumo[3][i],lumo[4][i],lumo[5][i],lumo[6][i],
                                                              lumo[7][i],lumo[8][i],lumo[9][i],lumo[10][i]))
output.close()


