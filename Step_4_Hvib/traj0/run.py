import os
import sys

# Fisrt, we add the location of the library to test to the PYTHON path
if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
import util.libutil as comn
from libra_py import DFTB_methods
from libra_py import units
from libra_py.workflows.nbra import step2_dftb

params = {
          "dt": 1.0 * units.fs2au ,
          "isnap":0 ,
          "fsnap":201 ,
         }

step2_dftb.run_step2_lz(params)


















