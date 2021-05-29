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
RootDir = 'F:/EDGAR/'
PointAddress = 'point_sources.xlsx'
file_name = find(RootDir)
count = len(file_name)
print(count)
# read the global point sources
point = pd.read_excel(PointAddress)
point = np.matrix(point)
point = np.column_stack([point, np.zeros([point.shape[0], 3])])
grid = np.zeros([point.shape[0], 2])
grid = np.matrix(grid)
grid[:, 0] = 900 - np.around(point[:, 0])/0.1
grid[:, 1] = np.around(point[:, 1])/0.1 + 1800
concentration = np.zeros([point.shape[0], point.shape[1] + count])
for i in range(0, count):
    f = Dataset(file_name[i])
    print(file_name[i])
    vcd = f.variables['emi_so2'][:]
    # unit is t/Gird/yr
    new_vcd = np.matrix(vcd)*3600*24*30*1000*11.12*11.12*12
    vcd = new_vcd
    vcd[:, 0:int(vcd.shape[1]/2)] = new_vcd[:, int(vcd.shape[1]/2):]
    vcd[:, int(vcd.shape[1]/2):] = new_vcd[:, 0:int(vcd.shape[1]/2)]
    vcd = vcd[::-1]
    np.nan_to_num(vcd)
    # rotate the matrix in inverse clockwise
    # vcd_lr = vcd[:, range(vcd.shape[1]-1, -1, -1)]
    # vcd = list(map(list, zip(*vcd_lr[::-1])))
    # vcd = np.matrix(vcd)
    for j in range(concentration.shape[0]):
        concentration[j, i+2] = vcd[int(grid[j, 0]), int(grid[j, 1])] + vcd[int(grid[j, 0])-1, int(grid[j, 1])-1] + \
                              vcd[int(grid[j, 0])-1, int(grid[j, 1])] + vcd[int(grid[j, 0])-1, int(grid[j, 1])+1] + \
                              vcd[int(grid[j, 0])+1, int(grid[j, 1])-1] + vcd[int(grid[j, 0])+1, int(grid[j, 1])] + \
                              vcd[int(grid[j, 0])+1, int(grid[j, 1])+1] + vcd[int(grid[j, 0]), int(grid[j, 1])+1] + \
                              vcd[int(grid[j, 0]), int(grid[j, 1])-1]
        concentration[j, i+2] = concentration[j, i+2]/9
        # define the missing value for delete
        if concentration[j, i+2] < -10.1:
            concentration[j, i+2] = -999
# np.savetxt('concentration.txt', concentration, fmt='%f')
f = openpyxl.Workbook()
sheet = f.active
sheet.title = 'concentration'
[h, l] = concentration.shape
for i in range(h):
    term = concentration[i, :].tolist()
    sheet.append(term)
f.save('EDGAR-concentraion.xlsx')
# -- Mann Kendall test -------------------------------------------------------------------------------------------------
for i in range(concentration.shape[0]):
    term = np.delete(concentration[i, 3:], np.where(concentration[i, 3:] == - 999))
    s, z, t = mk.mk_test(term, 1.28)
    point[i, 2] = s
    point[i, 3] = z
    point[i, 4] = t
f = xlwt.Workbook()
sheet2 = f.add_sheet('EDGAR_Mann-kendall_test')
[h, l] = point.shape
for i in range(h):
    for j in range(l):
        sheet2.write(i, j, point[i, j])
f.save('EDGAR-MK-test.xls')
# np.savetxt('trend.txt', point, fmt='%f')