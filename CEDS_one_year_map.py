from netCDF4 import Dataset
import xlsxwriter as xlwt
import find_file as find
import numpy as np


ceds_namelist = ['H:/OMI(Paper 1)/merra2_4x5_tropchem/GEOSChem.Restart.20130701_0000z.nc4',
                 'H:/OMI(Paper 1)/merra2_4x5_tropchem/GEOSChem.Restart.20140701_0000z.nc4']
para_num = ['SpeciesRst_SO2', 'lat', 'lon']
ceds_example = Dataset(ceds_namelist[0], format='NETCDF4')
mat = ceds_example.variables[para_num[0]][:]
lat = ceds_example.variables[para_num[1]][:]
lon = ceds_example.variables[para_num[2]][:]
ceds = np.zeros([mat.shape[2], mat.shape[3]])
time_count = 0
for i in range(len(ceds_namelist)):
    ceds_f = Dataset(ceds_namelist[i], format='NETCDF4')
    term_ceds = ceds_f.variables[para_num[0]][:]
    for j in range(term_ceds.shape[0]):
        ceds = ceds + term_ceds[j, 0, :, :]
        time_count = time_count + 1
ceds = ceds / time_count
workbook = xlwt.Workbook('ceds_oneyear.xlsx')
sheet = workbook.add_worksheet('Sheet1')
count = 1
for i in range(len(lat)):
    for j in range(len(lon)):
        sheet.write(count, 0, lat[i])
        sheet.write(count, 1, lon[j])
        sheet.write(count, 2, (ceds[i, j])*1e9*0.04089*64)
        count = count + 1
print('We area done!')
