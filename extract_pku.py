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
# define the properties of PKU-FUEL inventory.
# emission unit in kg/m2/s
# area in km2(0.1 degree)
# lat in degree(-90, 90)
# lon in degree(0, 360)
# ----------------------------------------------------------------------------------------------------------------------
ei_address = 'G:/PKU-FUEL/SO2/'
ei_suffix = '.nc'
variable_emi = 'emission'
variable_area = 'grid_cell_area'
variable_lat = 'lat'
variable_lon = 'lon'
begin_year = 2000
end_year = 2014
label_begin = -7
label_end = -3
degree = 0.1
ran = 10
namelist = ff.find_file(ei_address, ei_suffix)


# ----------------------------------------------------------------------------------------------------------------------
# point files load as numpy array, and find the emission inventory files.
# ----------------------------------------------------------------------------------------------------------------------
point_address = 'E:/Paper/coordinate.txt'
point = np.loadtxt(point_address)


# ----------------------------------------------------------------------------------------------------------------------
# read the emission in annual, output unit in KiloTons / year
# ----------------------------------------------------------------------------------------------------------------------
anl_emi = np.zeros([point.shape[0], point.shape[1] + end_year - begin_year + 1])
region_emi = np.zeros([end_year - begin_year + 1, 6])
anl_emi[:, 0:2] = point
count = 0
for i in range(len(namelist)):
    term_year = int(namelist[i][label_begin:label_end])
    if term_year <= end_year and term_year >= begin_year:
        print(namelist[i])
        f = Dataset(namelist[i], format='NETCDF4')
        emission = f.variables[variable_emi][:]
        area = f.variables[variable_area][:]
        lat = f.variables[variable_lat][:]
        lon = f.variables[variable_lon][:] - 180
        for k in range(emission.shape[0]):
            emission[k, :, :] = np.multiply(emission[k, :, :]*3600*24*30/1000/1000, area*1000*1000)
        # for j in range(point.shape[0]):
        #    grid_x = int(np.argmin(abs(lat - point[j, 0])))
        #    grid_y = int(np.argmin(abs(lon - point[j, 1])))
            # for k in range(emission.shape[0]):
            term_emission = np.zeros([emission.shape[1], emission.shape[2]])
            term_emission[:, 0:int(emission.shape[2]/2)] = emission[k, :, int(emission.shape[2]/2):]
            term_emission[:, int(emission.shape[2] / 2):] = emission[k, :, 0:int(emission.shape[2] / 2)]
            region_emi[count, :] = region_emi[count, :] + rt.region_ext(term_emission, degree)
        count = count + 1
                # anl_emi[j, term_year - begin_year + 2] = anl_emi[j, term_year - begin_year + 2] + ge.extract(grid_x, grid_y, term_emission, ran)


# ----------------------------------------------------------------------------------------------------------------------
# out put the result
# ----------------------------------------------------------------------------------------------------------------------
workbook = xlrt.Workbook('PKU_trend.xlsx')
worksheet = workbook.add_worksheet()
for i in range(region_emi.shape[0]):
    for j in range(region_emi.shape[1]):
        worksheet.write(i, j, region_emi[i, j])
workbook.close()
