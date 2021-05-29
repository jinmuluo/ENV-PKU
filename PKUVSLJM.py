from netCDF4 import Dataset
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
PKU_Address = 'H:/PKU-FUEL/BaP_wild_fire/'
PKU_Namelist = ff.find_file(PKU_Address, '.nc')
PKU_long = len(PKU_Namelist)
example = Dataset(PKU_Namelist[0], 'r', format='NETCDF4')
mat = example.variables['emission'][:]
PKU_emission = np.zeros([mat.shape[1], mat.shape[2], PKU_long])
term = np.zeros([mat.shape[1], mat.shape[2]])
print('Load', PKU_long, 'files')
count = 0
for name in PKU_Namelist:
    f = Dataset(name, 'r', format='NETCDF4')
    mat = f.variables['emission'][:]
    area = f.variables['grid_cell_area'][:]
    for j in range(mat.shape[0]):
        term[:, 0:int(mat.shape[2]/2)] = mat[j, :, int(mat.shape[2]/2):]
        term[:, int(mat.shape[2]/2):] = mat[j, :,  0:int(mat.shape[2]/2)]
        PKU_emission[:, :, count] = PKU_emission[:, :, count] + np.multiply(term, area)/1000
    count = count + 1

" Load the LJM data set in unit, unit is kg/m2/s "
LJM_Address = 'H:/PAHs/0.25 deg/'
LJM_Namelist = ff.find_file(LJM_Address, '.nc')
LJM_long = len(LJM_Namelist)
example = Dataset(LJM_Namelist[0], 'r', format='NETCDF4')
mat = example.variables['BaP'][:]
LJM_emission = np.zeros([mat.shape[0], mat.shape[1], LJM_long])
print('Load', LJM_long, 'files')
count = 0
for name in LJM_Namelist:
    f = Dataset(name, 'r', format='NETCDF4')
    mat = f.variables['BaP'][:]
    area = f.variables['grid_area'][:]*1000*1000
    LJM_emission[:, :, count] = LJM_emission[:, :, count] + np.multiply(mat[:, :], area)*3600*24*365
    count = count + 1

" Load the modis all sector data set in unit, unit is kg/m2/s "
Modis_Address = 'H:/PAHs/v2019-05/'
new_degree = 1
Modis_Namelist = ff.find_file(Modis_Address, '.nc')
Modis_long = len(Modis_Namelist)
example = Dataset(Modis_Namelist[0], 'r', format='NETCDF4')
mat = example.variables['PG_SRCE__POPG'][:]
Modis_emission = np.zeros([mat.shape[1], mat.shape[2], Modis_long])
print('Load', Modis_long, 'files')
modis_area = np.zeros([int(180/new_degree), int(360/new_degree)])
modis_area[:, :] = 111.31 *new_degree * 111.31 * new_degree
for i in range(modis_area.shape[0]):
    modis_area[i, :] = modis_area[i, :] * np.cos((90 - new_degree/2 - new_degree*i)*np.pi/180)
count = 0
for name in Modis_Namelist:
    f = Dataset(name, 'r', format='NETCDF4')
    mat = f.variables['PG_SRCE__POPG'][:]
    Modis_emission[:, :, count] = Modis_emission[:, :, count] + np.multiply(mat[0, :, :], modis_area*1000*1000)*3600*24*365
    count = count + 1

" Load the pku all sector data set in unit, unit is kg/m2/s "
pku_Address = 'H:/PAHs/v2019-04/'
new_degree = 1
pku_Namelist = ff.find_file(pku_Address, '.nc')
pku_long = len(pku_Namelist)
example = Dataset(pku_Namelist[0], 'r', format='NETCDF4')
mat = example.variables['PG_SRCE__POPG'][:]
pku2_emission = np.zeros([mat.shape[1], mat.shape[2], pku_long])
print('Load', pku_long, 'files')
pku_area = np.zeros([int(180/new_degree), int(360/new_degree)])
pku_area[:, :] = 111.31 * new_degree * 111.31 * new_degree
for i in range(pku_area.shape[0]):
    pku_area[i, :] = pku_area[i, :] * np.cos((90 - new_degree/2 - new_degree*i)*np.pi/180)
count = 0
for name in pku_Namelist:
    f = Dataset(name, 'r', format='NETCDF4')
    mat = f.variables['PG_SRCE__POPG'][:]
    pku2_emission[:, :, count] = pku2_emission[:, :, count] + np.multiply(mat[0, :, :], pku_area*1000*1000)*3600*24*365
    count = count + 1


"output the data set in your select range."
North = 90
South = 0
PKU_degree = 0.1
LJM_degree = 0.25
PKU_up = int((90 + South)/PKU_degree)
PKU_down = int((90 + North)/PKU_degree)
LJM_up = int((90 + South)/LJM_degree)
LJM_down = int((90 + North)/LJM_degree)
new_up = int((90 + South)/new_degree)
new_down = int((90 + North)/new_degree)
workbook = xlrt.Workbook('emission_north.xlsx')
worksheet = workbook.add_worksheet()
for i in range(PKU_emission.shape[2]):
    worksheet.write(i, 1, sum(sum(PKU_emission[PKU_up:PKU_down, :, i])))
    worksheet.write(i, 2, sum(sum(pku2_emission[new_up:new_down, :, i])))
    worksheet.write(i, 3, sum(sum(LJM_emission[LJM_up:LJM_down, :, i])))
    worksheet.write(i, 4, sum(sum(Modis_emission[new_up:new_down, :, i])))
workbook.close()

Ca_left = -167
Ca_right = -50
Eu_left = -10
Eu_right = 33
Ru_left = 33
Ru_right = 180
workbook = xlrt.Workbook('emission_3boreal_north.xlsx')
worksheet = workbook.add_worksheet()
for i in range(PKU_emission.shape[2]):
    worksheet.write(i, 0, sum(sum(PKU_emission[PKU_up:PKU_down, int((180 + Ca_left)/0.1):int((180 + Ca_right)/0.1), i])))
    worksheet.write(i, 1, sum(sum(PKU_emission[PKU_up:PKU_down, int((180 + Eu_left)/0.1):int((180 + Eu_right)/0.1), i])))
    worksheet.write(i, 2, sum(sum(PKU_emission[PKU_up:PKU_down, int((180 + Ru_left)/0.1):int((180 + Ru_right)/0.1), i])))
    worksheet.write(i, 3, sum(sum(LJM_emission[LJM_up:LJM_down, int((180 + Ca_left)/0.25):int((180 + Ca_right)/0.25), i])))
    worksheet.write(i, 4, sum(sum(LJM_emission[LJM_up:LJM_down, int((180 + Eu_left)/0.25):int((180 + Eu_right)/0.25), i])))
    worksheet.write(i, 5, sum(sum(LJM_emission[LJM_up:LJM_down, int((180 + Ru_left)/0.25):int((180 + Ru_right)/0.25), i])))

    worksheet.write(i, 6, sum(
        sum(Modis_emission[new_up:new_down, int((180 + Ca_left) / 1):int((180 + Ca_right) / 1), i])))
    worksheet.write(i, 7, sum(
        sum(Modis_emission[new_up:new_down, int((180 + Eu_left) / 1):int((180 + Eu_right) / 1), i])))
    worksheet.write(i, 8, sum(
        sum(Modis_emission[new_up:new_down, int((180 + Ru_left) / 1):int((180 + Ru_right) / 1), i])))

    worksheet.write(i, 9, sum(
        sum(pku2_emission[new_up:new_down, int((180 + Ca_left) / 1):int((180 + Ca_right) / 1), i])))
    worksheet.write(i, 10, sum(
        sum(pku2_emission[new_up:new_down, int((180 + Eu_left) / 1):int((180 + Eu_right) / 1), i])))
    worksheet.write(i, 11, sum(
        sum(pku2_emission[new_up:new_down, int((180 + Ru_left) / 1):int((180 + Ru_right) / 1), i])))
workbook.close()
