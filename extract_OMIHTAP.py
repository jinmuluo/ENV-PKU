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
# define the properties of OMI-HTAP inventory.
# emission unit in kg/m2/s
# area in km2(0.1 degree)
# lat in degree(-90, 90)
# lon in degree(-180, 180)
# ----------------------------------------------------------------------------------------------------------------------
ei_address = 'G:/OMI-HTAP/v2019-01/'
ei_suffix = '.nc4'
variable_emi = 'sanl1'
variable2_emi = 'sanl2'
variable_lat = 'lat'
variable_lon = 'lon'
begin_year = 2005
end_year = 2014
label_begin = -18
label_end = -14
degree = 0.1
ran = 12
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
anl_emi = np.zeros([point.shape[0], point.shape[1] + end_year - begin_year + 1])
anl_emi[:, 0:2] = point
region_emi = np.zeros([end_year - begin_year + 1, 6])
count = 0
for i in range(len(namelist)):
    term_year = int(namelist[i][label_begin:label_end])
    if term_year <= end_year and term_year >= begin_year:
        print(namelist[i])
        year = int(namelist[i][-18:-14])
        f = Dataset(namelist[i], format='NETCDF4')
        if namelist[i][-40:-33] == 'surface':
            emission = f.variables[variable_emi][:]
        else:
            emission = f.variables[variable2_emi][:]
        lat = f.variables[variable_lat][:]
        lon = f.variables[variable_lon][:]
        for k in range(emission.shape[0]):
            emission[k, :, :] = np.multiply(emission[k, :, :]*3600*24*30/1000/1000, area*1000*1000)
        #for j in range(point.shape[0]):
            #grid_x = int(np.argmin(abs(lat - point[j, 0])))
            #grid_y = int(np.argmin(abs(lon - point[j, 1])))
            #for k in range(emission.shape[0]):
                #term = np.multiply(emission[k, :, :] * 3600 * 24 * 30 / 1000 / 1000, area * 1000 * 1000)
                #anl_emi[j, term_year - begin_year + 2] = anl_emi[j, term_year - begin_year + 2 ] + ge.extract(grid_x, grid_y, term, ran)
            region_emi[year-begin_year, :] = region_emi[year-begin_year, :] + rt.region_ext(emission[k, :, :], degree)


# ----------------------------------------------------------------------------------------------------------------------
# out put the result
# ----------------------------------------------------------------------------------------------------------------------
workbook = xlrt.Workbook('OMI-HTAP_trend.xlsx')
worksheet = workbook.add_worksheet()
for i in range(region_emi.shape[0]):
    for j in range(region_emi.shape[1]):
        worksheet.write(i, j, region_emi[i, j])
workbook.close()
