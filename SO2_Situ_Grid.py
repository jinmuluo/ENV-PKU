import numpy as np
import xlsxwriter as xlwt
import xlrd


"""
This python files is writen for grid the situ measurement SO2 concentration into grid map
.
Author: Luo Jinmu
Email:myjinmuluo@pku.edu.cn
Organization: Urban and Environmental Science, Peking University, China

"""

# ----------------------------------------------------------------------------------------------------------------------
# Define the data set address and some predefine parameters
# ----------------------------------------------------------------------------------------------------------------------
Address = 'E:/OMI/measurement/Result_US_month.xlsx'
sheet_name = 'Sheet1'
lat_col = 4
lon_col = 5
month_num = 12
output_address = 'USA_4x5_MONTH.xlsx'
parameter = ['lat', 'lon', 'so2']
lat = np.arange(-90, 94, 4)
lat[0] = 89
lat[-1] = -89
lon = np.arange(-180, 180, 5)

# ----------------------------------------------------------------------------------------------------------------------
# Grid the point sources into maps
# ----------------------------------------------------------------------------------------------------------------------
mat = np.zeros([month_num, len(lat), len(lon)])
count = np.zeros([month_num, len(lat), len(lon)])
f = xlrd.open_workbook(Address)
sheet = f.sheet_by_name(sheet_name)
latitude = sheet.col_values(lat_col)
longitude = sheet.col_values(lon_col)
for i in range(0, month_num):
    sulphur = sheet.col_values(i+lon_col+1)
    for j in range(1, len(sulphur)):
        for k in range(len(lat)):
            if (lat[k] - 2) < float(latitude[j]) < (lat[k] + 2):
                y = k
                break
            elif k == len(lat) - 1:
                print("Can not find this latitude in look up table", latitude[j])
        for k in range(len(lon)):
            if (lon[k]-2.5) < float(longitude[j]) < (lon[k]+2.5):
                x = k
                break
            elif k == len(lon) - 1:
                print("Can not find this longitude in look up table", longitude[j])
        if type(sulphur[j]) == type('abc'):
            continue
        mat[i, y, x] = mat[i, y, x] + float(sulphur[j])
        count[i, y, x] = count[i, y, x] + 1
    print('---------- ', i/len(sulphur)*100, '%--------')
count[count == 0] = 1
for i in range(mat.shape[0]):
    mat[i, :, :] = np.divide(mat[i, :, :], count[i, :, :])

# ----------------------------------------------------------------------------------------------------------------------
# Output the data set
# ----------------------------------------------------------------------------------------------------------------------
fw = xlwt.Workbook(output_address)
sheet = fw.add_worksheet('so2_measurement')
cc = 1
sheet.write(0, 0, 'latitude')
sheet.write(0, 1, 'longitude')
sheet.write(0, 2, 'sulphur dioxide')
for i in range(len(lat)):
    for j in range(len(lon)):
        if max(mat[:, i, j]) <= 0.0000001:
            continue
        else:
            sheet.write(cc, 0, lat[i])
            sheet.write(cc, 1, lon[j])
            for k in range(mat.shape[0]):
                sheet.write(cc, 2 + k, mat[k, i, j])
        cc = cc + 1
print('Done!')








