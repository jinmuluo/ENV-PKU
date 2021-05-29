from netCDF4 import Dataset
import numpy as np
import find_file as find
import xlrd
import xlsxwriter as xlwt

# ----------------------------------------------------------------------------------------------------------------------
# This python files is written for GEOS-Chem 12.3.2 output, when the every day files is separate form each others.
# ----------------------------------------------------------------------------------------------------------------------

GC_data_address = 'H:/OMI(Paper 1)/GEOS-Chem/PKU/'
coordinate_address = 'E:/OMI/measurement/Coordinate.xlsx'
output_address = 'GC_USA_pku_days.xlsx'

workbook = xlrd.open_workbook(coordinate_address)
sheet = workbook.sheet_by_name('USA')
lat = sheet.col_values(0)
lon = sheet.col_values(1)
op_workbook = xlwt.Workbook(output_address)
op_sheet = op_workbook.add_worksheet('GEOS-Chem')
suffix = 'nc4'
para_name = ['SpeciesRst_SO2']
# t_name = 'BXHGHT-$::T'
# pressure_name = 'BXHGHT-$::PEDGE'
geos_chem_namelist = find.find_file(GC_data_address, suffix)
print('Load', len(geos_chem_namelist), 'files in address:', GC_data_address, '! ')
count = 1

op_sheet.write(0, 0, 'Lat')
op_sheet.write(0, 1, 'Lon')
for i in range(len(geos_chem_namelist)):
    op_sheet.write(0, i + 2, str(geos_chem_namelist[i][-18:-10]))

for i in range(len(geos_chem_namelist)):
    f = Dataset(geos_chem_namelist[i], format='NETCDF4')
    sulphur = np.zeros([])
    for parameter in para_name:
        # tem = f.select(t_name).get()
        # pre = f.select(pressure_name).get() / 10
        sulphur = sulphur + f.variables[parameter][:] * 1e9 * 0.04089 * 64
    latitude = f.variables['lat'][:]
    longitude = f.variables['lon'][:]
    for j in range(1, len(lat)):
        if i == 0:
            op_sheet.write(j, 0, lat[j])
            op_sheet.write(j, 1, lon[j])
# ----------------------------------------------------- Need change ----------------------------------------------------
        y = np.where(abs(longitude - lon[j]) <= 2.50)
        x = np.where(abs(latitude - lat[j]) <= 2.0)
# ----------------------------------------------------------------------------------------------------------------------
        op_sheet.write(j, i + 2, sulphur[0, 0, x[0][0], y[0][0]])
print('we are done!')









