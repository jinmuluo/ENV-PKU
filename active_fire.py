import numpy as np
from pyhdf.SD import SD, SDC
import xlsxwriter as xlwt
import find_file as find


"""
This python file is writen for Sum the Modis active fire map

"""


address = 'H:/MOD14CMH(active fire)/'
suffix = '.hdf'
variable = 'MeanPower'
namelist = find.find_file(address, suffix)
print('Found', len(namelist), 'files')
mat = np.zeros([])
for file in namelist:
    f = SD(file, SDC.READ)
    mat = mat + f.select(variable).get()
lat = np.arange(90, -90, -0.5)
lon = np.arange(-180, 180, 0.5)

ex_f = xlwt.Workbook('active_fire.xlsx')
sheet = ex_f.add_worksheet()

sheet.write(0, 0, 'lat')
sheet.write(0, 1, 'lon')
sheet.write(0, 2, 'MeanPower')
count = 1
for i in range(len(lat)):
    for j in range(len(lon)):
        if mat[i, j] <= 1:
            print('skip')
        else:
            sheet.write(count, 0, lat[i])
            sheet.write(count, 1, lon[j])
            sheet.write(count, 2, mat[i, j])
            count = count + 1
ex_f.close()
