# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 14:26:51 2017

@author: sigurdja
"""

import os
import matplotlib.pyplot as plt

import psspy
import dyntools
import redirect
from psse_models import load_models

_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()
redirect.psse2py()

psspy.throwPsseExceptions = True

# Files and folders
cwd = os.getcwd()
models = os.path.join(cwd, "models")

casefile = os.path.join(models, "Scenario1.sav")
dyrfile = os.path.join(models, "Scenario1.dyr")
outputfile = os.path.join(cwd, "output.out")

psspy.psseinit(10000)


# Initiation----------------------------------------------------------------------------------------------------------------------------------
psspy.case(casefile)
psspy.dyre_new([1, 1, 1, 1], dyrfile, "", "", "")

psspy.cong(0)
psspy.conl(0, 1, 1, [0, 0], [50.0, 50.0, 0.0, 100.0])
psspy.conl(0, 1, 2, [0, 0], [50.0, 50.0, 0.0, 100.0])
psspy.conl(0, 1, 3, [0, 0], [50.0, 50.0, 0.0, 100.0])
psspy.dynamics_solution_params(realar=[_f, _f, 0.005, _f, _f, _f, _f, _f])

psspy.machine_array_channel([1, 2, 6000])  # Monitor Kvilldal Power
psspy.machine_array_channel([2, 7, 6000])  # Monitor Kvilldal Frequency

ierr = psspy.strt(outfile=outputfile)  # initialize dynamic simulation

# Simulation----------------------------------------------------------------------------------------------------------------------------------
t = 1
T = 600
dt = 60
steps = int(T/dt)

load = load_models.Load(6500)

if ierr == 0:
    psspy.run(tpause=0, nprt=0, nplt=0)
    load.step(100)
    psspy.run(tpause=120)


else:
        print(ierr)

chnf = dyntools.CHNF(outputfile)
sh_ttl, ch_id, ch_data = chnf.get_data()

plt.figure(1)
plt.plot(ch_data['time'], ch_data[1])  # Kvilldal Power

plt.figure(2)
plt.plot(ch_data['time'], ch_data[2])  # Kvilldal frequency

plt.show()
