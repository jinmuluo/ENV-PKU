from pyhdf.SD import SD, SDC
import numpy as np
import find_file as find
import xlsxwriter as xlrt
import matplotlib.pyplot as plt
import pandas as pd


# ----------------------------------------------------------------------------------------------------------------------
# Step 1: define the basic information about the data
# ----------------------------------------------------------------------------------------------------------------------
category = 'MODIS'
target_address = 'H:/ModisFire/Russian/hdf/'
output_address = 'H:/ModisFire/Russian_PAHs.xlsx'
suffix = '.hdf'
namelist = find.find_file(target_address, suffix)
var_name = ['IJ-AVG-$::POPG', 'IJ-AVG-$::POPPBCPI', 'IJ-AVG-$::POPPBCPO', 'IJ-AVG-$::POPPOCPI', 'IJ-AVG-$::POPPOCPO']
t_name = 'BXHGHT-$::T'
pressure_name = 'BXHGHT-$::PEDGE'
# air_density = 'BXHGHT-$::AIRNUMDE'
long = len(namelist)
print('Found', long, 'Files! in', target_address)

# ----------------------------------------------------------------------------------------------------------------------
# Step 2:define the position need to be outputted, in 4x5 GEOS-Chem out put;
# alert_x = 24, alert_y = 43; zeppelin_x = 38, zeppelin_y = 42; pallas_x = 41, pallas_y = 39, pallas_y2 = 40;
# Niembro_x = 21,Niembro_y = 35; Beijing_x = 59, Beijing_y = 33; Aspvreten_x = 37,Aspvreten_y = 39;
# ----------------------------------------------------------------------------------------------------------------------
place = 4
level_num = 1
alert_x = 24
alert_y = 43
zeppelin_x = 38
zeppelin_y = 42
pallas_x = 41
pallas_y = 39
pallas_y2 = 40

# ----------------------------------------------------------------------------------------------------------------------
# Step 3:extract the data, ( BaP 252.316; 1mol/mol = 1e9*11.2638 ng/m3 ; 11.2638 = 252.316/22.4)
# 1 mol/mol = 1e6 ppm = 1e9 ppb
# ug/m3 = 0.04089 x concentration(ppb) x molecular weight
# (1) ug/m3 = 1 ppbV x molecular weight(g/mols) /8.3144 /Temperature(K) x air pressure(kPa)
# (2) 1 mol/mol = le9 * 0.04089 * 252.316 * le6 pg/m3 --> 1 BaP mol/mol= 10.3196728e15 BaP pg/m3
# ----------------------------------------------------------------------------------------------------------------------
matrix = np.zeros([])
# matrix = np.zeros([12, 47, 90, 144])
concentration = np.zeros([long, place])
count = 0
for i in range(long):
    f = SD(namelist[i], SDC.READ)
    year = namelist[i][-19:-15]
    month = namelist[i][-15:-13]

    # add the gas phase and particulate phase together.
    for k in range(len(var_name)):
        if k == 0:
            matrix = f.select(var_name[k]).get()
        else:
            matrix = matrix + f.select(var_name[k]).get()
    # extract the temperature and air pressure,notice the original unit: temperature is K, but Pressure is hPa.
    tem = f.select(t_name).get()
    pre = f.select(pressure_name).get()/10
    # air_den = f.select(air_density).get()

    # change the unit ppbV into pg/m3
    # matrix = np.multiply(matrix*(1e9)/6.02e23*252.316, air_den)
    matrix = np.multiply(np.divide(matrix * 252.316/8.3144, tem), pre)*1000*1000

    # output the result in month base.
    concentration[count, 0] = int(str(year + str(month)))
    print('Searching the', str(year + str(month)), 'file!')
    for level in range(level_num):
        concentration[count, 1] = concentration[count, 1] + matrix[level, alert_y, alert_x]
        concentration[count, 2] = concentration[count, 2] + matrix[level, zeppelin_y, zeppelin_x]
        concentration[count, 3] = concentration[count, 3] + matrix[level, pallas_y, pallas_x]
        concentration[count, 3] = concentration[count, 3] + matrix[level, pallas_y2, pallas_x]
        concentration[count, 3] = concentration[count, 3]/2
    count = count + 1


# ----------------------------------------------------------------------------------------------------------------------
# Step 4:create an excel file to storage the data set.
# ----------------------------------------------------------------------------------------------------------------------
if long == 0:
    print('zeros files found, so not excel output remains.')
    exit(0)
wb = xlrt.Workbook(output_address)
ws = wb.add_worksheet()
for i in range(concentration.shape[0]):
    for j in range(concentration.shape[1]):
        ws.write(i, j, concentration[i, j])
wb.close()



























