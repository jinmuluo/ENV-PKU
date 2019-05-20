from netCDF4 import Dataset
import ggplot as gplt
import numpy as np
import find_file as ff
import xlsxwriter as xlrt


"""
This python file is write for compare PKU-FUEL-BaP with my BaP emission inventory
author: Jinmu Luo
Email: myjinmuluo@pku.edu.cn/gmail.com/163.com
Time:2019/3/5
"""


" Load the PKU-FUEL data set, unit is in g /km2 /month"
PKU_Address = 'G:/PKU-FUEL/BaP_wild_fire/'
PKU_Namelist = ff.find_file(PKU_Address, '.nc')
PKU_long = len(PKU_Namelist)
example = Dataset(PKU_Namelist[0], 'r', format='NETCDF4')
mat = example.variables['emission'][:]
PKU_emission = np.zeros([mat.shape[1], mat.shape[2], PKU_long])
print('Load', PKU_long, 'files')
count = 0
for name in PKU_Namelist:
    f = Dataset(name, 'r', format='NETCDF4')
    mat = f.variables['emission'][:]
    area = f.variables['grid_cell_area'][:]
    for j in range(mat.shape[0]):
        PKU_emission[:, :, count] = PKU_emission[:, :, count] + np.multiply(mat[j, :, :], area)/1000/1000
    count = count + 1


" Load the LJM data set in unit, unit is kg/m2/s "
LJM_Address = 'G:/PAHs/0.25 deg/'
LJM_Namelist = ff.find_file(LJM_Address, '.nc')
LJM_long = len(LJM_Namelist)
example = Dataset(LJM_Namelist[0], 'r', format='NETCDF4')
mat = example.variables['BaP'][:]
LJM_emission = np.zeros([mat.shape[0], mat.shape[1], LJM_long])
print('Load',LJM_long, 'files')
count = 0
for name in LJM_Namelist:
    f = Dataset(name, 'r', format='NETCDF4')
    mat = f.variables['BaP'][:]
    area = f.variables['grid_area'][:]*1000*1000
    LJM_emission[:, :, count] = LJM_emission[:, :, count] + np.multiply(mat[:, :], area)*3600*24*365/1000
    count = count + 1

"output the data set in your select range."
North = 90
South = 45
PKU_degree = 0.1
LJM_degree = 0.25
PKU_up = int((90 - North)/PKU_degree)
PKU_down = int((90 - South)/PKU_degree)
LJM_up = int((90 - North)/LJM_degree)
LJM_down = int((90 - South)/LJM_degree)
workbook = xlrt.Workbook('emission.xlsx')
worksheet = workbook.add_worksheet()
for i in range(PKU_emission.shape[2]):
    worksheet.write(i, 1, sum(sum(PKU_emission[PKU_up:PKU_down, :, i])))
    worksheet.write(i, 2, sum(sum(LJM_emission[LJM_up:LJM_down, :, i])))
workbook.close()
