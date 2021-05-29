import xlsxwriter as xlwt
import xlrd
import numpy as np


# define the daily data set.
data_address = 'E:/OMI/measurement/USEPA/daily_42401_2014.xlsx'
f = xlrd.open_workbook(data_address)
sheet = f.sheet_by_name('daily_42401_2014')
state = sheet.col_values(0)
country = sheet.col_values(1)
site = sheet.col_values(2)
lat = sheet.col_values(5)
lon = sheet.col_values(6)
standard = sheet.col_values(10)
sulphur = sheet.col_values(16)
result_list = []
now_state = state[1]
now_country = site[1]
now_site = site[1]
now_sulphur = float(sulphur[1])
year_sulphur = np.zeros([12, 1])
count = 1
row = 1
now_time = xlrd.xldate_as_tuple(sheet.cell(1, 11).value, 0)
# define the output file
f_output = xlwt.Workbook('Result_US_month.xlsx')
Result_sheet = f_output.add_worksheet()
Result_sheet.write(0, 0, 'state')
Result_sheet.write(0, 1, 'country')
Result_sheet.write(0, 2, 'site')
Result_sheet.write(0, 3, 'year')
Result_sheet.write(0, 4, 'lat')
Result_sheet.write(0, 5, 'lon')
Result_sheet.write(0, 6, 'january')
Result_sheet.write(0, 7, 'february')
Result_sheet.write(0, 8, 'march')
Result_sheet.write(0, 9, 'april')
Result_sheet.write(0, 10, 'may')
Result_sheet.write(0, 11, 'june')
Result_sheet.write(0, 12, 'july')
Result_sheet.write(0, 13, 'august')
Result_sheet.write(0, 14, 'september')
Result_sheet.write(0, 15, 'october')
Result_sheet.write(0, 16, 'november')
Result_sheet.write(0, 17, 'december')

for i in range(2, len(sulphur)):
    time = xlrd.xldate_as_tuple(sheet.cell(i, 11).value, 0)
    if standard[i] == 'SO2 3-hour 1971':
        continue

    if state[i] == now_state and country[i] == now_country and site[i] == now_site and time[1] == now_time[1]:
        now_sulphur = now_sulphur + float(sulphur[i])
        count = count + 1
    else:
        if state[i] != now_state or country[i] != now_country or site[i] != now_site:
            print(state[i - 1], country[i - 1], site[i - 1], now_time[0], now_time[1], now_sulphur, count)
            Result_sheet.write(row, 0, state[i - 1])
            Result_sheet.write(row, 1, country[i - 1])
            Result_sheet.write(row, 2, site[i - 1])
            Result_sheet.write(row, 3, now_time[0])
            Result_sheet.write(row, 4, lat[i - 1])
            Result_sheet.write(row, 5, lon[i - 1])
            now_sulphur = now_sulphur / count
            count = 1
            Result_sheet.write(row, int(now_time[1]) + 5, now_sulphur)
            row = row + 1
            now_state = state[i]
            now_country = country[i]
            now_site = site[i]
            now_time = xlrd.xldate_as_tuple(sheet.cell(i, 11).value, 0)
            now_sulphur = float(sulphur[i])
        else:
            now_sulphur = now_sulphur/count
            count = 1

            # ug/m3 = 0.04089 x concentration(ppb) x molecular weight(SO2 = 64)
            Result_sheet.write(row, int(now_time[1]) + 5, now_sulphur*2.61696)
            now_state = state[i]
            now_country = country[i]
            now_site = site[i]
            now_time = xlrd.xldate_as_tuple(sheet.cell(i, 11).value, 0)
            now_sulphur = float(sulphur[i])

print('Done!')
