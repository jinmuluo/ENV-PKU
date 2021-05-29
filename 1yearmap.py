import numpy as np
from pyhdf.SD import SD, SDC
import find_file as find
import xlsxwriter as xlwt


data_address = 'H:/ModisFire/MODIS_wildfire/hdf/'
output_address = 'ave_map.xlsx'
suffix = '.hdf'
namelist = find.find_file(data_address, suffix)
print('Find', len(namelist), 'files in address:', data_address)
var_name = ['IJ-AVG-$::POPG', 'IJ-AVG-$::POPPBCPI', 'IJ-AVG-$::POPPBCPO', 'IJ-AVG-$::POPPOCPI', 'IJ-AVG-$::POPPOCPO']
t_name = 'BXHGHT-$::T'
pressure_name = 'BXHGHT-$::PEDGE'
matrix = np.zeros([])
for file in namelist:
    print('Deal the', file)
    f = SD(file, SDC.READ)
    dat = np.zeros([])
    for i in range(len(var_name)):
        dat = dat + f.select(var_name[i]).get()
    tem = f.select(t_name).get()
    pre = f.select(pressure_name).get() / 10
    dat = np.multiply(np.divide(dat * 252.316 / 8.3144, tem), pre) * 1000 * 1000
    matrix = matrix + dat

f = SD(namelist[0], SDC.READ)
lat = f.select('LAT').get()
lon = f.select('LON').get()
matrix = matrix/len(namelist)

f_out = xlwt.Workbook(output_address)
ws = f_out.add_worksheet()
count = 0
for i in range(len(lat)):
    for j in range(len(lon)):
        ws.write(count, 0, lat[i])
        ws.write(count, 1, lon[j])
        ws.write(count, 2, matrix[0, i, j])
        count = count + 1




