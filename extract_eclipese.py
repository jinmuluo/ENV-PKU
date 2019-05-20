import numpy as np
from netCDF4 import Dataset
import find_file as ff
import grid_extract as ge
import xlsxwriter as xlrt
import region_trend as rt
"""
This python file is writen for extract the emission for any inventory through know point
author: Jinmu Luo
time:2019/3/31
email: myjinmuluo@pku.edu.cn/163.com/gmail.com

"""

# ----------------------------------------------------------------------------------------------------------------------
# define the properties of ECLIPSEv5a inventory.
# emission unit in kt/yr
# area in km2(0.5 degree)
# lat in degree(-90, 90)
# lon in degree(-180, 180)
# ----------------------------------------------------------------------------------------------------------------------
ei_address = 'G:/Eclipse/'
ei_suffix = '.nc'
variable_emi = 'emis_all'
variable_lat = 'lat'
variable_lon = 'lon'
begin_year = 2005
end_year = 2014
degree = 0.5
ran = 2
namelist = ff.find_file(ei_address, ei_suffix)

# ----------------------------------------------------------------------------------------------------------------------
# point files load as numpy array, and find the emission inventory files.
# ----------------------------------------------------------------------------------------------------------------------
point_address = 'E:/Paper/coordinate.txt'
point = np.loadtxt(point_address)


# ----------------------------------------------------------------------------------------------------------------------
# read the emission in annual, output unit in KiloTons / year
# ----------------------------------------------------------------------------------------------------------------------
# anl_emi = np.zeros([point.shape[0], point.shape[1] + 11])
# anl_emi[:, 0:2] = point
region_emi = np.zeros([11, 6])
for i in range(len(namelist)):
    print(namelist[i])
    f = Dataset(namelist[i], format='NETCDF4')
    emission = f.variables[variable_emi][:]
    lat = f.variables[variable_lat][:]
    lon = f.variables[variable_lon][:]
    for k in range(emission.shape[0]):
        # for j in range(point.shape[0]):
            # grid_x = int(np.argmin(abs(lat - point[j, 0])))
            # grid_y = int(np.argmin(abs(lon - point[j, 1])))
            # anl_emi[j, k + 2] = anl_emi[j, k + 2] + ge.extract(grid_x, grid_y, emission[k, :, :], ran)
        region_emi[k, :] = rt.region_ext(emission[k, :, :], degree)



# ----------------------------------------------------------------------------------------------------------------------
# out put the result
# ----------------------------------------------------------------------------------------------------------------------
workbook = xlrt.Workbook('Eclipese_trend.xlsx')
worksheet = workbook.add_worksheet()
for i in range(region_emi.shape[0]):
    for j in range(region_emi.shape[1]):
        worksheet.write(i, j, region_emi[i, j])
workbook.close()
