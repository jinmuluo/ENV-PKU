import find_file as find
import numpy as np
from netCDF4 import Dataset
import math
import xlsxwriter as xlwt


"""
This python files is created for construct the wind direction EXCEL file.
Author: Luo Jinmu
Email: myjinmuluo@pku.edu.cn

"""


address = 'E:/ModisFire/windmap/'
suffix = '.nc'
namelist = find.find_file(address, suffix)
print('Found', len(namelist), 'files')
u_file = Dataset(namelist[0])
u_wind = u_file.variables['uwnd'][:]
v_file = Dataset(namelist[1])
v_wind = v_file.variables['vwnd'][:]
lat = v_file.variables['lat'][:]
lon = v_file.variables['lon'][:]
result = np.zeros([len(lat)*len(lon), 4])
count = 0
for i in range(len(lat)):
    for j in range(len(lon)):
        result[count, 0] = lat[i]
        if lon[j] > 180:
            result[count, 1] = lon[j] - 360
        else:
            result[count, 1] = lon[j]
        result[count, 2] = np.sqrt(u_wind[0, i, j]*u_wind[0, i, j] + v_wind[0, i, j]*v_wind[0, i, j])
        result[count, 3] = math.atan(u_wind[0, i, j]/(v_wind[0, i, j]+0.0001))*180/np.pi
        if result[count, 3] < 0:
            result[count, 3] = 180 - result[count, 3]
        count = count + 1

f = xlwt.Workbook('windmap.xlsx')
sheet = f.add_worksheet()
for i in range(result.shape[0]):
    sheet.write(i, 0, result[i, 0])
    sheet.write(i, 1, result[i, 1])
    sheet.write(i, 2, result[i, 2])
    sheet.write(i, 3, result[i, 3])
f.close()
