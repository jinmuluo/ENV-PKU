import numpy as np
import mk_test as mk
import xlsxwriter as xlwt


target_address = 'E:/OMI/GRAPH_data/mk_test/CEDS.txt'
result_address = 'E:/OMI/GRAPH_data/mk_test/result.xlsx'
matrix = data = np.genfromtxt(target_address)
result = np.zeros([matrix.shape[0], 3])
mk_level = 1.28
for i in range(result.shape[0]):
    result[i, :] = mk.mk_test(matrix[i, :], mk_level)

workbook = xlwt.Workbook(result_address)
worksheet = workbook.add_worksheet()
for i in range(result.shape[0]):
    worksheet.write(i, 0, result[i, 0])
    worksheet.write(i, 1, result[i, 1])
    worksheet.write(i, 2, result[i, 2])
workbook.close()
