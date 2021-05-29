import numpy as np
import os
import pandas as pd
from netCDF4 import Dataset
import mk_test as mk
import openpyxl
import xlwt


def find(RootDir):
    file_name = list()
    for root, dirs, files in os.walk(RootDir):
        for file in files:
            file_name.append(os.path.join(root, file))
        for dir in dirs:
            find(dir)
    return(file_name)


# ---------- main code -------------------------------------------------------------------------------------------------
RootDir = 'G:/OMI/OMIL3/'
PointAddress = 'point_sources.xlsx'
file_name = find(RootDir)
days = len(file_name)
print(days)
# read the global point sources
point = pd.read_excel(PointAddress)
point = np.matrix(point)
point = np.column_stack([point, np.zeros([point.shape[0], 3])])
grid = np.zeros([point.shape[0], 2])
grid = np.matrix(grid)
grid[:, 0] = 360 - np.around(point[:, 0])/0.25
grid[:, 1] = np.around(point[:, 1])/0.25 + 720
concentration = np.zeros([point.shape[0], point.shape[1] + days])
for i in range(2, days):
    f = Dataset(file_name[i])
    print(file_name[i])
    vcd = f.variables['ColumnAmountSO2_PBL'][:]
    vcd = vcd[::-1]
    vcd = np.matrix(vcd)
    np.nan_to_num(vcd)
    # rotate the matrix in inverse clockwise
    # vcd_lr = vcd[:, range(vcd.shape[1]-1, -1, -1)]
    # vcd = list(map(list, zip(*vcd_lr[::-1])))
    # vcd = np.matrix(vcd)
    for j in range(concentration.shape[0]):
        concentration[j, i] = vcd[int(grid[j, 0]), int(grid[j, 1])] + vcd[int(grid[j, 0])-1, int(grid[j, 1])-1] + \
                              vcd[int(grid[j, 0])-1, int(grid[j, 1])] + vcd[int(grid[j, 0])-1, int(grid[j, 1])+1] + \
                              vcd[int(grid[j, 0])+1, int(grid[j, 1])-1] + vcd[int(grid[j, 0])+1, int(grid[j, 1])] + \
                              vcd[int(grid[j, 0])+1, int(grid[j, 1])+1] + vcd[int(grid[j, 0]), int(grid[j, 1])+1] + \
                              vcd[int(grid[j, 0]), int(grid[j, 1])-1]
        concentration[j, i] = concentration[j, i]/9
        # define the missing value for delete
        if concentration[j, i] < -10.1:
            concentration[j, i] = -999
# np.savetxt('concentration.txt', concentration, fmt='%f')
f = openpyxl.Workbook()
sheet = f.active
sheet.title = 'concentration'
[h, l] = concentration.shape
for i in range(h):
    term = concentration[i, :].tolist()
    sheet.append(term)
f.save('concentraion.xlsx')
# -- Mann Kendall test -------------------------------------------------------------------------------------------------
for i in range(concentration.shape[0]):
    term = np.delete(concentration[i, 3:], np.where(concentration[i, 3:] == - 999))
    s, z, t = mk.mk_test(term, 1.28)
    point[i, 2] = s
    point[i, 3] = z
    point[i, 4] = t
f = xlwt.Workbook()
sheet2 = f.add_sheet('Mann-kendall_test')
[h, l] = point.shape
for i in range(h):
    for j in range(l):
        sheet2.write(i, j, point[i, j])
f.save('MK-test.xls')
# np.savetxt('trend.txt', point, fmt='%f')
