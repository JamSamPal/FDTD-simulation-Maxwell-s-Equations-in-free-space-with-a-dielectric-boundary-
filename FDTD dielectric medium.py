# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 09:55:36 2024

@author: James
"""

#FDTD 1D solver for Maxwell's Equations with a dielectric medium over half the domain
'''This program injects a source signal into a FDTD solver for Maxwell's
Equations
in free space with a dielectric boundary and outputs the 1D space containing
the
2 electomagnetic field components to a file (located in the user's working
directory).
It then creates a folder called 'Snapshots' that contains graphs of the
Electric field
at different times, also located in the user's working directory.
Additionally a plot of
the E-field and H-fields at spatial step 50 are plotted and finally a
waterfall
plot is produced and saved, once again, to the user's working directory.'''


''' Importing modules'''
import numpy as np
import matplotlib.pyplot as plt
'''Extra modules imported to make file reading and saving easier'''
import csv
import pandas as pd
import os
import shutil


'''Creating directory for snapshots'''
Dir = 'Snapshots'
if not os.path.exists(Dir): #If no folder exists, make one, otherwise otherwrite the existing one
    os.makedirs(Dir)
else:
    shutil.rmtree(Dir)
    os.makedirs(Dir)
    
    
'''Initialising data'''
f = 50 #Framerate, i.e. how often snapshots of the Electric field are taken
n = 200 #Spatial domain width
t = 0
max_t = 1000 + f + 1 #Maximum time domain value that will allow graphs up to t =1000 to be plotted
E = np.zeros([n])
H = np.zeros([n])
space = np.linspace(0, n, n)
file = open("EM_Data_for_k=50.csv", "w")
file_2 = open("EM_Data_snapshots.csv", "w")
writer = csv.writer(file, delimiter = ',')
writer_2 = csv.writer(file_2, delimiter = ',')
Title = 'Timestep', 'E[50] field component (V/m)', 'H[50] field component (A/m)'
Title_2 = 'Timestep', 'E field component (V/m)', 'H field component (A/m)'
writer.writerow(Title)
writer_2.writerow(Title_2)
reader = csv.reader(file)
reader_2 = csv.reader(file_2)


'''FDTD solver script'''
while t < max_t:
    H[:-1] += E[:-1] - E[1:]  #H field evolution
    for k in range(1,n): #Iterating E field over all space, starting at E[1] as E[0] is initialised later on
        if k < 100: #Setting up dielectric boundary halfway along the domain
            ep = 1
        else:
            ep = 9 #Setting ep at 9 (sqrt(ep) = n, the refractive index, this was choosen as 3 to simplify the maths)
        E[k] = E[k] + (H[k-1] - H[k])/ep
    if t%f == 0: #Snapshot loop
        for k in range (1,n):
                D = t, E[k], H[k]
                writer_2.writerow(D) #Write snapshot data to CSV file
    E[0] = np.exp(-(t - 30.) * (t - 30.) / 100.) #Initialising E field as a gaussian pulse
    P = t, E[50], H[50] #Writing snapshot at spacestep k = 50
    writer.writerow(P)
    t += 1


'''Writing and reading the data accrued'''
df = pd.read_csv("EM_Data_for_k=50.csv") #Using panda module to read csv files with ease
T = df['Timestep']
E = df['E[50] field component (V/m)']
H = df['H[50] field component (A/m)']
plt.figure() #Graph for E field at k = 50
plt.xlabel('Timestep')
plt.ylabel('E[50] field component (V/m)')
plt.grid()
plt.plot(T,E)
plt.savefig('E[50] plot')
plt.figure() #Graph for H field at k = 50
plt.xlabel('Timestep')
plt.ylabel('H[50] field component (A/m)')
plt.grid()
plt.plot(T,H)
plt.savefig('H[50] plot')
df_2 = pd.read_csv("EM_Data_snapshots.csv")


'''Loop to save snapshots'''
max_value = ((max_t -1)/50)*n #Value one needs to iterate up to to produce graphs up to t = 1000
for i in range (0, int(max_value) ,n): #i going up in sets of 200, i.e. 0-199, 200-399... every set of 200 points is 1 snapshot
    E_2 = df_2.loc[i:(i+n-1), 'E field component (V/m)'] #Indexing with the panda module to find E field values in E field column
    T_2 = df_2.loc[int(i), 'Timestep']
    plt.figure()
    plt.xlabel('Spacestep')
    plt.ylabel('E field component (V/m)')
    plt.plot([100, 100], [-1, 1], 'k-', lw=2) #Plotting a line to indicate the dielectric medium boundary
    plt.title('Snapshot at t = ' + str(T_2))
    plt.grid()
    plt.plot(space, E_2)
    plt.savefig('Snapshots/snapshot' + str(int(T_2)))
    plt.close()



'''Waterfall plot''' #(the plot in the report used f = 25)
fig = plt.figure()
ax = fig.add_subplot(111)
for i in range (0, int(max_value), 200):
    ax.plot(space, df_2.loc[i:(i+n-1),'E field component (V/m)'] + (i/200), 'b')
    #Plotting multiple snapshots over one another with a slight vertical offset.
    plt.xlabel('Spacestep')
    plt.ylabel('Time [frame number]')
    plt.savefig('Waterfall normal')
    plt.show()
