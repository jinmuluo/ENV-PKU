import numpy as np
import find_file as find
import xlsxwriter as xlrt
from netCDF4 import Dataset

# ----------------------------------------------------------------------------------------------------------------------
# Step 1: define the basic information about the data
# ----------------------------------------------------------------------------------------------------------------------
target_address = 'H:/ModisFire/PKU_2002-2010/nc/'
output_address = 'H:/ModisFire/pku_PAHs_nc.xlsx'
suffix = '.nc'
namelist = find.find_file(target_address, suffix)
var_name = ['SPC_POPG', 'SPC_POPPBCPI', 'SPC_POPPBCPO', 'SPC_POPPOCPI', 'SPC_POPPOCPO']
long = len(namelist)
print('Found', long, 'Files!')

# ----------------------------------------------------------------------------------------------------------------------
# Step 2:define the position need to be outputted.
# ----------------------------------------------------------------------------------------------------------------------
place = 5
level_num = 1
alert_x = 24
alert_y = 43
zeppelin_x = 38
zeppelin_y = 42
pallas_x = 41
pallas_y = 39
pallas_y2 = 40

# ----------------------------------------------------------------------------------------------------------------------
# Step 3:extract the data, ( BaP 252.316; 1mol/mol = 1e9*11.2638 ng/m3 ; 11.2638 = 252.316/22.4)
# 1 mol/mol = 1e6 ppm = 1e9 ppb
# ug/m3 = 0.04089 x concentration(ppb) x molecular weight
# (1) ug/m3 = 1 ppbV x molecular weight(g/mols) /8.3144 /Temperature(K) x air pressure(kPa)
# (2) 1 mol/mol = le9 * 0.04089 * 252.316 * le6 pg/m3 --> 1 BaP mol/mol= 10.3196728e15 BaP pg/m3
# ----------------------------------------------------------------------------------------------------------------------
matrix = np.zeros([])
# matrix = np.zeros([12, 47, 90, 144])
concentration = np.zeros([long, place])
count = 0
for i in range(long):
    f = Dataset(namelist[i], 'r', format='NETCDF4')
    year = namelist[i][-15:-11]
    month = namelist[i][-11:-9]

    # add the gas phase and particulate phase together.
    for k in range(len(var_name)):
        if k == 0:
            matrix = f.variables[var_name[k]][:]
        else:
            matrix = matrix + f.variables[var_name[k]][:]

    # change the unit mol/mol into pg/m3
    matrix = matrix*1e9*11.2638*1000*1000

    # output the result in month base.
    concentration[count, 0] = int(str(year + str(month)))
    print('Searching the', str(year + str(month)), 'file!')
    for level in range(level_num):
        concentration[count, 1] = concentration[count, 1] + matrix[0, level, alert_y, alert_x]
        concentration[count, 2] = concentration[count, 2] + matrix[0, level, zeppelin_y, zeppelin_x]
        concentration[count, 3] = concentration[count, 3] + matrix[0, level, pallas_y, pallas_x]
        concentration[count, 4] = concentration[count, 4] + matrix[0, level, pallas_y2, pallas_x]
    count = count + 1


# ----------------------------------------------------------------------------------------------------------------------
# Step 4:create an excel file to storage the data set.
# ----------------------------------------------------------------------------------------------------------------------
if long == 0:
    print('zeros files found, so not excel output remains.')
    exit(0)
wb = xlrt.Workbook(output_address)
ws = wb.add_worksheet()
for i in range(concentration.shape[0]):
    for j in range(concentration.shape[1]):
        ws.write(i, j, concentration[i, j])
wb.close()
