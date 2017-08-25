# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 14:26:51 2017

@author: sigurdja
"""

import os  # I use this to work with files

import psspy  # Import the psse module
import dyntools  # Import the dynamic simulation module
import redirect  # Module for redirecting the PSS/E output to the terminal
import xlsxwriter # For writing to excel
from psse_models import load_models  # The load models

# Define default PSS/E variables
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()

# Redirect the PSS/E output to the terminal
redirect.psse2py()

psspy.throwPsseExceptions = True

# Files and folders
cwd = os.getcwd()  # Get the current directory
models = os.path.join(cwd, "models")  # Name of the folder with the models

# Names of the case files
casefile = os.path.join(models, "Scenario1.sav")
dyrfile = os.path.join(models, "Scenario1.dyr")

# Name of the file where the dynamic simulation output is stored
outputfile = os.path.join(cwd, "output.out")

# Start PSS/E
psspy.psseinit(10000)

# Initiation----------------------------------------------------------------------------------------------------------------------------------
psspy.case(casefile)  # Read in the power flow data
psspy.dyre_new([1, 1, 1, 1], dyrfile, "", "", "")

# Convert the loads for dynamic simulation
psspy.cong(0)
psspy.conl(0, 1, 1, [0, 0], [50.0, 50.0, 0.0, 100.0])
psspy.conl(0, 1, 2, [0, 0], [50.0, 50.0, 0.0, 100.0])
psspy.conl(0, 1, 3, [0, 0], [50.0, 50.0, 0.0, 100.0])

# Set the time step for the dynamic simulation
psspy.dynamics_solution_params(realar=[_f, _f, 0.005, _f, _f, _f, _f, _f])

psspy.machine_array_channel([1, 2, 6000])  # Monitor Kvilldal Power
psspy.machine_array_channel([2, 7, 6000])  # Monitor Kvilldal Frequency

ierr = psspy.strt(outfile=outputfile)  # Tell PSS/E to write to the output file

# List all in service buses
sid = 1

# Create subsystem based on voltage range
sid = psspy.bsys(1, 1, [0, 1000])

# Get bus numbers
load_ids = test = psspy.alodbusint(1, 2, 'NUMBER')[1][0]

# Standard deviation of the loads
sd = 0.001

# Simulation parameters
t = 1  # Start time of the simulation
T = 90  # End time of the simulation
dt = 1  # How often to step the load
steps = int(T/dt)   # Calculate how many times the loads should be stepped
pmu_td = 4  # To tell PSS/E to write to screen and file at PMU frequency

# Make all the loads in the system into Wiener proceesses
loads = [load_models.WienerProcessLoad(load_num, steps, sd, dt)
         for load_num in load_ids]

ierr = psspy.strt(outfile=outputfile)  # Tell PSS/E to write to the output file

# Simulation----------------------------------------------------------------------------------------------------------------------------------
if ierr == 0:
    # Start the simulation
    psspy.run(tpause=0, nprt=pmu_td, nplt=pmu_td)

    # Iterate over the load steps
    for j in range(1, steps):
        psspy.run(tpause=j*dt, nprt=pmu_td, nplt=pmu_td)
        # Iterate over all the loads and step them
        for load in loads:
            load.step(j)
else:
    print(ierr)

# Read the putput file
chnf = dyntools.CHNF(outputfile)
# assign the data to variables
sh_ttl, ch_id, ch_data = chnf.get_data()

# Write to excel
book = xlsxwriter.Workbook('example.xlsx')  # Create the excel workbook
sheet = book.add_worksheet()  # Add sheet
sheet.write(0, 0,'Time')
sheet.write(0, 1,'Power')
sheet.write(0, 2, 'Frequency')
row = 1

# There may be some smarter way than using a loop, but it works
for t, p, f in zip(ch_data['time'], ch_data[1], ch_data[2]):
	sheet.write(row, 0, t)
	sheet.write(row, 1, p)
	sheet.write(row, 2, f)
	row = row + 1

book.close()
