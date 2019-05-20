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
# define the properties of CEDS inventory.
# emission unit in kg/m2/s
# area in km2(0.5 degree)
# lat in degree(-90, 90)
# lon in degree(0, 360)
# ----------------------------------------------------------------------------------------------------------------------
ei_address = 'G:/CEDS/'
ei_suffix = '.nc'
variable_emi1 = 'SO2_agr'
variable_emi2 = 'SO2_ene'
variable_emi3 = 'SO2_ind'
variable_emi4 = 'SO2_rco'
variable_emi5 = 'SO2_shp'
variable_emi6 = 'SO2_slv'
variable_emi7 = 'SO2_tra'
variable_emi8 = 'SO2_wst'
variable_lat = 'lat'
variable_lon = 'lon'
begin_year = 2000
end_year = 2014
label_begin = -7
label_end = -3
degree = 0.5
ran = 2
namelist = ff.find_file(ei_address, ei_suffix)
area = np.zeros([int(180/degree), int(360/degree)])
for i in range(area.shape[0]):
    area[i, :] = 111.31*degree*111.31*degree*np.cos((90 - degree/2 - i*degree)*np.pi/180)

# ----------------------------------------------------------------------------------------------------------------------
# point files load as numpy array, and find the emission inventory files.
# ----------------------------------------------------------------------------------------------------------------------
point_address = 'E:/Paper/coordinate.txt'
point = np.loadtxt(point_address)


# ----------------------------------------------------------------------------------------------------------------------
# read the emission in annual, output unit in KiloTons / year
# ----------------------------------------------------------------------------------------------------------------------
# anl_emi = np.zeros([point.shape[0], point.shape[1] + end_year - begin_year + 1])
# anl_emi[:, 0:2] = point
region_emi = np.zeros([end_year - begin_year + 1, 6])
count = 0
for i in range(len(namelist)):
    term_year = int(namelist[i][label_begin:label_end])
    if term_year <= end_year and term_year >= begin_year:
        print(namelist[i])
        f = Dataset(namelist[i], format='NETCDF4')
        emission1 = f.variables[variable_emi1][:]
        emission2 = f.variables[variable_emi2][:]
        emission3 = f.variables[variable_emi3][:]
        emission4 = f.variables[variable_emi4][:]
        emission5 = f.variables[variable_emi5][:]
        emission6 = f.variables[variable_emi6][:]
        emission7 = f.variables[variable_emi7][:]
        emission8 = f.variables[variable_emi8][:]
        emission = emission1 + emission2 + emission3 + emission4 + emission5 + emission6 + emission7 + emission8
        lat = f.variables[variable_lat][:]
        lon = f.variables[variable_lon][:]
        for k in range(emission.shape[0]):
            emission[k, :, :] = np.multiply(emission[k, :, :]*3600*24*30/1000/1000, area*1000*1000)
        # for j in range(point.shape[0]):
            # for k in range(emission.shape[0]):
                # grid_x = int(np.argmin(abs(lat - point[j, 0])))
                # grid_y = int(np.argmin(abs(lon - point[j, 1])))
                # anl_emi[j, term_year - begin_year + 2] = anl_emi[j, term_year - begin_year + 2 ] + ge.extract(grid_x, grid_y, emission[k, :,:], ran)
            region_emi[count, :] = region_emi[count, :] + rt.region_ext(emission[k, :, :], degree)
        count = count + 1
# ----------------------------------------------------------------------------------------------------------------------
# out put the result
# ----------------------------------------------------------------------------------------------------------------------
workbook = xlrt.Workbook('CEDS_trend.xlsx')
worksheet = workbook.add_worksheet()
for i in range(region_emi.shape[0]):
    for j in range(region_emi.shape[1]):
        worksheet.write(i, j, region_emi[i, j])
workbook.close()
