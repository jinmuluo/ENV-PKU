import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data_address = 'E:/ModisFire/GRAPH_DATA/'
ym_data = data_address + 'year&month_trend.txt'
ca_season = data_address + 'ca_seasonal_trend.txt'
eu_season = data_address + 'eu_seasonal_trend.txt'
ru_season = data_address + 'ru_seasonal_trend.txt'

# read the data as pandas data frame.
ym = pd.read_table(ym_data)
ca_sea = pd.read_table(ca_season)
eu_sea = pd.read_table(eu_season)
ru_sea = pd.read_table(ru_season)

# plot the year trend of three boreal forest
term = np.array(ym.year)
year = term[0:17]
month = term[17:]
term = np.array(ym.Ca)
ca_year = term[0:17]
ca_month = term[17:]
term = np.array(ym.Eu)
eu_year = term[0:17]
eu_month = term[17:]
term = np.array(ym.Ru)
ru_year = term[0:17]
ru_month = term[17:]
term = np.array(ym.total)
total_year = term[0:17]
total_month = term[17:]

y = np.vstack([ca_year, eu_year, ru_year])
labels = ["Ca boreal ", "Eu boreal", "Ru boreal"]
plt.stackplot(year, y/1000, labels=labels)
plt.legend(loc='upper left')
plt.xlabel('Year', size=30)
plt.title('Northern boreal forest ', size=30)
plt.ylabel('Burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.show()

y = np.vstack([ca_month, eu_month, ru_month])
labels = ["Ca boreal ", "Eu boreal", "Ru boreal"]
plt.stackplot(month, y/1000, labels=labels)
plt.legend(loc='upper left')
plt.xlabel('Month', size=30)
plt.title('Northern boreal forest ', size=30)
plt.ylabel('Monthly mean burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.show()


exit(0)
plt.plot(year, total_year/1000, c='purple', alpha=0.8)
plt.title('Northern boreal forest ', size=30)
plt.xlabel('Year', size=30)
plt.ylabel('Burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.grid()
plt.show()

plt.plot(month, total_month/1000, c='purple', alpha=0.8)
plt.title('Northern boreal forest ', size=30)
plt.xlabel('Month', size=30)
plt.ylabel('Monthly mean burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.grid()
plt.show()

plt.plot(year, ca_year/1000, c='red', alpha=0.8)
plt.title('Canadian boreal forest ', size=30)
plt.xlabel('Year', size=30)
plt.ylabel('Burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.grid()
plt.show()

plt.plot(month, ca_month/1000, c='red', alpha=0.8)
plt.title('Canadian boreal forest ', size=30)
plt.xlabel('Month', size=30)
plt.ylabel('Monthly mean burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.grid()
plt.show()

plt.plot(year, eu_year/1000, c='blue', alpha=0.8)
plt.title('European boreal forest ', size=30)
plt.xlabel('Year', size=30)
plt.ylabel('Burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.grid()
plt.show()

plt.plot(month, eu_month/1000, c='blue', alpha=0.8)
plt.title('European boreal forest ', size=30)
plt.xlabel('Month', size=30)
plt.ylabel('Month mean burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.grid()
plt.show()

plt.plot(year, ru_year/1000, c='green', alpha=0.8)
plt.title('Russian boreal forest ', size=30)
plt.xlabel('Year', size=30)
plt.ylabel('Burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.grid()
plt.show()

plt.plot(month, ru_month/1000, c='green', alpha=0.8)
plt.title('Russian boreal forest ', size=30)
plt.xlabel('Month', size=30)
plt.ylabel('Monthly mean burned area (10^3 hectare)', size=30)
plt.yticks(fontproperties='Times New Roman', size=25)
plt.xticks(fontproperties='Times New Roman', size=25)
plt.grid()
plt.show()