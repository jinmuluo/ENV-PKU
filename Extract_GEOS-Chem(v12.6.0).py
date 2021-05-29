from netCDF4 import Dataset
import numpy as np
import xlrd
import xlsxwriter as xlwt
# ----------------------------------------------------------------------------------------------------------------------
# This python files is written for GEOS-Chem 12.6.0, when the every day files is cluster in to one or two files.
# ----------------------------------------------------------------------------------------------------------------------
GC_data_address = ['H:/OMI(Paper 1)/merra2_4x5_tropchem/GEOSChem.Restart.20130701_0000z.nc4',
                   'H:/OMI(Paper 1)/merra2_4x5_tropchem/GEOSChem.Restart.20140701_0000z.nc4']
coordinate_address = 'E:/OMI/measurement/Coordinate.xlsx'
output_address = 'CEDS_USA_days.xlsx'

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
print('Load', len(GC_data_address), 'files!')
count = 1

op_sheet.write(0, 0, 'Lat')
op_sheet.write(0, 1, 'Lon')
months_count = 0
for i in range(len(GC_data_address)):
    f = Dataset(GC_data_address[i], format='NETCDF4')
    sulphur = np.zeros([])
    for parameter in para_name:
        # tem = f.select(t_name).get()
        # pre = f.select(pressure_name).get() / 10
        sulphur = sulphur + f.variables[parameter][:] * 1e9 * 0.04089 * 64
    if i == 0:
        months_count = 0
    else:
        f_term = Dataset(GC_data_address[i-1], format='NETCDF4')
        variable_term = f_term.variables[para_name[0]][:]
        months_count = months_count + variable_term .shape[0]
    print(months_count)

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
        for months in range(sulphur.shape[0]):
            op_sheet.write(j, i + 2 + months_count + months, sulphur[months, 0, x[0][0], y[0][0]])

print('we are done!')
