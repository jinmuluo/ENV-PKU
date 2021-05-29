import xlsxwriter as xlwt
import xlrd


data_address = 'E:/OMI/measurement/USEPA/daily_42401_2014.xlsx'
f = xlrd.open_workbook(data_address)
sheet = f.sheet_by_name('daily_42401_2014')
state = sheet.col_values(0)
country = sheet.col_values(1)
site = sheet.col_values(2)
lat = sheet.col_values(5)
lon = sheet.col_values(6)
time = sheet.col_values(11)
standard = sheet.col_values(10)
sulphur = sheet.col_values(17)
result_list = []
now_state = state[1]
now_country = site[1]
now_site = site[1]
now_sulphur = float(sulphur[1])
count = 1
for i in range(2, len(sulphur)):
    if standard[i] == 'SO2 3-hour 1971':
        continue
    if state[i] == now_state and country[i] == now_country and site[i] == now_site:
        now_sulphur = now_sulphur + float(sulphur[i])
        count = count + 1
    else:
        result_list.append(state[i-1])
        result_list.append(country[i-1])
        result_list.append(site[i-1])
        result_list.append(lat[i-1])
        result_list.append(lon[i-1])
        now_sulphur = now_sulphur/count
        print(state[i-1], country[i-1], site[i-1], now_sulphur, count)
        count = 1
        result_list.append(now_sulphur)
        now_state = state[i]
        now_country = country[i]
        now_site = site[i]
        now_sulphur = float(sulphur[i])

f = xlwt.Workbook('Result_US.xlsx')
Result_sheet = f.add_worksheet()
Result_sheet.write(0, 0, state[0])
Result_sheet.write(0, 1, country[0])
Result_sheet.write(0, 2, site[0])
Result_sheet.write(0, 3, lat[0])
Result_sheet.write(0, 4, lon[0])
Result_sheet.write(0, 5, sulphur[0])
for i in range(1, int(len(result_list)/6)):
    Result_sheet.write(i, 0, result_list[0 + i*6])
    Result_sheet.write(i, 1, result_list[i*6 + 1])
    Result_sheet.write(i, 2, result_list[i*6 + 2])
    Result_sheet.write(i, 3, result_list[i*6 + 3])
    Result_sheet.write(i, 4, result_list[i*6 + 4])
    Result_sheet.write(i, 5, result_list[i*6 + 5])
print('Done!')