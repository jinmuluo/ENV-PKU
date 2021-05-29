import numpy as np
import xlsxwriter as xlwt
import xlrd

data_address = \
['E:/OMI/measurement/EastAsia/station.xlsx',
 'E:/OMI/measurement/EastAsia/2014-05.xlsx',
 'E:/OMI/measurement/EastAsia/2014-06.xlsx',
 'E:/OMI/measurement/EastAsia/2014-07.xlsx',
 'E:/OMI/measurement/EastAsia/2014-08.xlsx',
 'E:/OMI/measurement/EastAsia/2014-09.xlsx',
 'E:/OMI/measurement/EastAsia/2014-10.xlsx',
 'E:/OMI/measurement/EastAsia/2014-11.xlsx',
 'E:/OMI/measurement/EastAsia/2014-12.xlsx']

goal_station = xlrd.open_workbook(data_address[0])
sheet = goal_station.sheet_by_name('Sheet1')
goal_site = sheet.col_values(1)
goal_city = sheet.col_values(2)
month = np.zeros([len(goal_city) - 1, len(data_address) - 1])

for i in range(1, len(data_address)):
    print(data_address[i])
    data = xlrd.open_workbook(data_address[i])
    data_sheet = data.sheet_by_name(data_address[i][-12:-5])
    city = data_sheet.col_values(1)
    site = data_sheet.col_values(2)
    sulphur = data_sheet.col_values(8)
    for j in range(1, len(goal_city)):
        now_city = goal_city[j]
        now_site = goal_site[j]
        count = 1
        for k in range(1, len(sulphur)):
            if type(sulphur[k]) == type('abc'):
                continue
            if city[k] == now_city and site[k] == now_site:
                month[j-1, i-1] = month[j-1, i-1] + float(sulphur[k])
                count = count + 1
        print('Month', data_address[i][-7:-5], ' -------- ', j/len(goal_city)*100, '% --------------------')
        month[j-1, i-1] = month[j-1, i-1]/count

workbook = xlwt.Workbook('Result_month.xlsx')
sheet = workbook.add_worksheet()
for i in range(month.shape[0]):
    for j in range(month.shape[1]):
        sheet.write(i, j, month[i, j])
print('Done!')










