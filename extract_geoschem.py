from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import find_file as find
import xlsxwriter as xlrt


# define the basic information about data
target_address = 'G:/GEOS-Chem/reault/'
output_address = 'G:/GEOS-Chem/reault/alert.xlsx'
namelist = find.find_file(target_address, '.nc')
var_name = 'emi'
long = len(namelist)

# define the position need to output
alert_x = 1
alert_y = 2

# extract the data
for i in range(long):
    f = Dataset(namelist[i], 'r', format='NETCDF4')
    matrix = f.variables[var_name][:]


# create an excel file to storage the dataset.
wb = xlrt.Workbook(output_address)
ws = wb.add_worksheet()

