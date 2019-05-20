import numpy as np
from pyhdf.SD import SD, SDC
import find_file as f
import matplotlib.pyplot as plt
import xlsxwriter as xlwt
"""
This python file is written for plot the trend of modis burned area in boreal forest region

"""
address = 'G:/MCD64CMQ(burned area)/C6/'
namelist = f.find_file(address, '.hdf')
date = len(namelist)
result = np.zeros([date, 4])
degree = 0.25
# define the range of three type boreal forest
Euleft = 680
Euright = 860
Ruleft = 861
Ruright = 1339
Caleft = 0
Caright = 480

for i in range(date):
    f = SD(namelist[i], SDC.READ)
    year = namelist[i][-29:-25]
    day = namelist[i][-25:-22]
    burned_area = f.select('BurnedArea').get()
    result[i, 0] = int(year)*1000+int(day)
    result[i, 1] = sum(sum(burned_area[0:200, Caleft:Caright]))*0.01
    result[i, 2] = sum(sum(burned_area[0:200, Euleft:Euright]))*0.01
    result[i, 3] = sum(sum(burned_area[0:200, Ruleft:Ruright]))*0.01

workbook = xlwt.Workbook('modis_fire_trend.xlsx')
worksheet = workbook.add_worksheet()
for i in range(result.shape[0]):
    worksheet.write(i, 0, result[i, 0])
    worksheet.write(i, 1, result[i, 1])
    worksheet.write(i, 2, result[i, 2])
    worksheet.write(i, 3, result[i, 3])
workbook.close()

