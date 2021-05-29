from netCDF4 import Dataset
import xlsxwriter as xlwt
import find_file as find
import numpy as np


omi_address = 'H:/OMI(Paper 1)/GEOS-Chem/OMI/'
pku_address = 'H:/OMI(Paper 1)/GEOS-Chem/PKU/'
suffix = 'nc4'
omi_namelist = find.find_file(omi_address, suffix)
print('Found', len(omi_namelist), 'in address:', omi_address)
pku_namelist = find.find_file(pku_address, suffix)
print('Found', len(pku_namelist), 'in address:', pku_address)
para_num = ['SpeciesRst_SO2', 'lat', 'lon']

if len(omi_namelist) != len(pku_namelist):
    print('Keep the time range similar!!')
    exit(0)

omi_example = Dataset(omi_namelist[0], format='NETCDF4')
mat = omi_example.variables[para_num[0]][:]
lat = omi_example.variables[para_num[1]][:]
lon = omi_example.variables[para_num[2]][:]
omi = np.zeros([mat.shape[2], mat.shape[3]])
pku = np.zeros([mat.shape[2], mat.shape[3]])
for i in range(len(omi_namelist)):
    omi_f = Dataset(omi_namelist[i], format='NETCDF4')
    term_omi = omi_f.variables[para_num[0]][:]
    omi = omi + term_omi[0, 0, :, :]
    pku_f = Dataset(pku_namelist[i], format='NETCDF4')
    term_pku = pku_f.variables[para_num[0]][:]
    pku = pku + term_pku[0, 0, :, :]
omi = omi / len(omi_namelist)
pku = pku / len(pku_namelist)

workbook = xlwt.Workbook('pku_oneyear.xlsx')
sheet = workbook.add_worksheet('Sheet1')
count = 1
for i in range(len(lat)):
    for j in range(len(lon)):
        sheet.write(count, 0, lat[i])
        sheet.write(count, 1, lon[j])
        sheet.write(count, 2, (pku[i, j])*1e9*0.04089*64)
        print(omi[i, j]*1e9*0.04089*64, pku[i, j]*1e9*0.04089*64)
        count = count + 1
print('We area done!')
