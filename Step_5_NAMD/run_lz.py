import os
import sys
import time
import math


if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
from libra_py import *
import libra_py.workflows.nbra.step4 as step4
import libra_py.workflows.nbra.lz as lz

from libra_py import units
import libra_py.workflows.nbra.step4 as step4
import libra_py.workflows.nbra.lz as lz
import libra_py.workflows.nbra.decoherence_times as decoherence_times
from libra_py import data_conv
from libra_py import fit
from libra_py import influence_spectrum as infsp

# For details of params, check the documentation for lz.py under libra NBRA workflows
params = {}

trajs = range(1)
params["data_set_paths"] = []
for itraj in trajs:
    params["data_set_paths"].append("traj" + str(itraj) + "/res/")

params["nstates"] = 596
params["nfiles"]  = 199
params["Hvib_re_prefix"] = "hvib_"; params["Hvib_re_suffix"] = "_re"
params["Hvib_im_prefix"] = "hvib_"; params["Hvib_im_suffix"] = "_im"
params["active_space"]       = range(params["nstates"])
params["target_space"]       = 1
params["T"]                  = 300.0
params["dt"]                 = 1.0*units.fs2au
params["nsteps"]             = params["nfiles"]
params["init_times"]         = [0]
params["do_output"]          = True
params["do_return"]          = False
params["ntraj"]              = 1
params["tdse_Ham"]           = 1
params["sh_method"]          = 1
params["evolve_Markov"]      = True
params["evolve_TSH"]         = False
params["decoherence_method"] = 0
params["Boltz_opt"] = 0
params["Boltz_opt_BL"]       = 1
params["gap_min_exception"]  = 0

start = time.time()
Hvib = step4.get_Hvib2(params)
init_time = params["init_times"][0]
end = time.time()
print("Time to read / assemble data = ", end - start)

tau, rates = decoherence_times.decoherence_times_ave(Hvib, [init_time], params["nfiles"]-init_time, 0)
avg_deco = tau/units.fs2au

run_list = [309]

for lumo in run_list :
    params["istate"] = lumo
    params["outfile"] = str(lumo)+".txt"
    res = lz.run(Hvib, params)





