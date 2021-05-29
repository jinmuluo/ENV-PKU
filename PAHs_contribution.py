import numpy as np
import xlsxwriter as xlwt
from netCDF4 import Dataset
import find_file as find


# ----------------------------------------------------------------------------------------------------------------------
# define the data set address and read as a list.
# ----------------------------------------------------------------------------------------------------------------------

total_address = 'H:/PKU-FUEL/BaP/'
wildfire_address = 'H:/PKU-FUEL/BaP_wild_fire/'
total_name_list = find.find_file(total_address, '.nc')
wildfire_name_list = find.find_file(wildfire_address, '.nc')
print('Find', len(total_name_list), 'total emission files!')
print('Find', len(wildfire_name_list), 'wild fire emission files!')
degree = 0.1
time = len(total_name_list)

# ----------------------------------------------------------------------------------------------------------------------
# read the data set and storage emission as numpy matrix
# ----------------------------------------------------------------------------------------------------------------------
total = np.zeros([time, int(180/degree), int(360/degree)])
total_new = np.zeros([time, int(180/degree), int(360/degree)])
wildfire = np.zeros([time, int(180/degree), int(360/degree)])
wildfire_new = np.zeros([time, int(180/degree), int(360/degree)])
for i in range(time):
    total_f = Dataset(total_name_list[i], 'r', format='NETCDF4')
    wildfire_f = Dataset(wildfire_name_list[i], 'r', format='NETCDF4')
    total_emi = total_f.variables['emission'][:]
    wildfire_emi = wildfire_f.variables['emission'][:]
    area = total_f.variables['grid_cell_area'][:]
    for j in range(total_emi.shape[0]):
        total[i, :, :] = total[i, :, :] + np.multiply(total_emi[j, :, :], area) / 1000 / 1000
        wildfire[i, :, :] = wildfire[i, :, :] + np.multiply(wildfire_emi[j, :, :], area) / 1000 / 1000
for i in range(total.shape[0]):
    total_new[i, :, 0:int(total.shape[2]/2)] = total[i, :, int(total.shape[2]/2):]
    total_new[i, :, int(total.shape[2]/2):] = total[i, :, 0:int(total.shape[2]/2)]
    wildfire_new[i, :, 0:int(total.shape[2] / 2)] = wildfire[i, :, int(total.shape[2] / 2):]
    wildfire_new[i, :, int(total.shape[2] / 2):] = wildfire[i, :, 0:int(total.shape[2] / 2)]
print('Extract the emissoin!')

# ----------------------------------------------------------------------------------------------------------------------
# output region total emission from the data set as excel file(.xlsx)
# the grid is follow the WGS84 coordinate system.
# ----------------------------------------------------------------------------------------------------------------------
Northern = 89
Southern = 40
Ca_left = -167
Ca_right = -50
Eu_left = -10
Eu_right = 33
Ru_left = 33
Ru_right = 180
workbook = xlwt.Workbook('PAH_contribution.xlsx')
worksheet = workbook.add_worksheet()
for i in range(time):
    worksheet.write(i, 1, sum(sum(total_new[i, int((90 + Southern)/degree):int((90 + Northern)/degree), int((180 + Ca_left)/degree):int((180 + Ca_right)/degree)])))
    worksheet.write(i, 2, sum(sum(total_new[i, int((90 + Southern) / degree):int((90 + Northern) / degree), int((180 + Eu_left) / degree):int((180 + Eu_right) / degree)])))
    worksheet.write(i, 3, sum(sum(total_new[i, int((90 + Southern) / degree):int((90 + Northern) / degree), int((180 + Ru_left) / degree):int((180 + Ru_right) / degree)])))
    worksheet.write(i, 4, sum(sum(wildfire_new[i, int((90 + Southern) / degree):int((90 + Northern) / degree), int((180 + Ca_left) / degree):int((180 + Ca_right) / degree)])))
    worksheet.write(i, 5, sum(sum(wildfire_new[i, int((90 + Southern) / degree):int((90 + Northern) / degree),int((180 + Eu_left) / degree):int((180 + Eu_right) / degree)])))
    worksheet.write(i, 6, sum(sum(wildfire_new[i, int((90 + Southern) / degree):int((90 + Northern) / degree),int((180 + Ru_left) / degree):int((180 + Ru_right) / degree)])))
workbook.close()
print('Done!')
