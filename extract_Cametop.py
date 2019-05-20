import numpy as np
import xlsxwriter as xlrt
import find_file as ff


address = 'E:/ModisFire/PAHs/results/BaP_out1/'
namelist = ff.find_file(address, '.dat')
# alert:y = 172, x = 298 ;
# zeppelin : y = 168, x = 12 ;
# pallas : y = 158, x =  24;
y = 158
x = 24
result_matrix = np.zeros([len(namelist), 3])
i = 0
for file in namelist:
    pah = np.loadtxt(file, dtype=float)
    result_matrix[i, 0] = file[-11:-7]
    result_matrix[i, 1] = file[-6:-4]
    result_matrix[i, 2] = pah[(y-1)*360 + x - 1, 2]
    i = i + 1
    print('year:', file[-11:-7], 'month', file[-6:-4], pah[(y-1)*360 + x - 1, 2])


workbook = xlrt.Workbook('PAHs.xlsx')
worksheet = workbook.add_worksheet()
for i in range(result_matrix.shape[0]):
    worksheet.write(i, 1, result_matrix[i, 0])
    worksheet.write(i, 2, result_matrix[i, 1])
    worksheet.write(i, 3, result_matrix[i, 2])
workbook.close()
