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

plt.figure(figsize=(18, 14))
y = np.vstack([ca_year, eu_year, ru_year])
labels = ["Ca boreal ", "Eu boreal", "Ru boreal"]
plt.stackplot(year, y/100000, labels=labels)
plt.legend(loc='upper right', fontsize=40)
plt.title('Northern Boreal Forest ', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.xlabel('Year', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure1.jpeg', format='jpeg', dpi=300)

plt.figure(figsize=(18, 14))
y = np.vstack([ca_month, eu_month, ru_month])
labels = ["Ca boreal ", "Eu boreal", "Ru boreal"]
plt.stackplot(month, y/100000, labels=labels)
plt.legend(loc='upper left', fontsize=40)
plt.xlabel('Month', size=55)
plt.title('Northern Boreal Forest ', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure2.jpeg', format='jpeg', dpi=300)


plt.figure(figsize=(18, 14))
plt.plot(year, total_year/100000, c='purple', alpha=0.8,  linewidth=1)
plt.fill_between(year, total_year/100000-(total_year/100000).std(), total_year/100000+(total_year/100000).std(),
                 color='lightblue')
plt.title('Northern boreal forest ', size=55)
plt.xlabel('Year', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.grid()
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure3.jpeg', format='jpeg', dpi=300)

plt.figure(figsize=(18, 14))
plt.plot(month, total_month/100000, c='purple', alpha=0.8, linewidth=3)
plt.title('Northern Boreal Forest ', size=55)
plt.xlabel('Month', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.grid()
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure4.jpeg', format='jpeg', dpi=300)

plt.figure(figsize=(18, 14))
plt.plot(year, ca_year/100000, c='red', alpha=0.8, linewidth=1)
plt.fill_between(year, ca_year/100000-(ca_year/100000).std(), ca_year/100000+(ca_year/100000).std(), color='lightblue')
plt.title('Canadian Boreal Forest ', size=55)
plt.xlabel('Year', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.grid()
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure5.jpeg', format='jpeg', dpi=300)

plt.figure(figsize=(18, 14))
plt.plot(month, ca_month/100000, c='red', alpha=0.8, linewidth=3)
plt.title('Canadian Boreal Forest ', size=55)
plt.xlabel('Month', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.grid()
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure6.jpeg', format='jpeg', dpi=300)

plt.figure(figsize=(18, 14))
plt.plot(year, eu_year/100000, c='blue', alpha=0.8, linewidth=1)
plt.fill_between(year, eu_year/100000-(eu_year/100000).std(), eu_year/100000+(eu_year/100000).std(), color='lightblue')
plt.title('European Boreal Forest ', size=55)
plt.xlabel('Year', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.grid()
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure7.jpeg', format='jpeg', dpi=300)

plt.figure(figsize=(18, 14))
plt.plot(month, eu_month/100000, c='blue', alpha=0.8, linewidth=3)
plt.title('European Boreal Forest ', size=55)
plt.xlabel('Month', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.grid()
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure8.jpeg', format='jpeg', dpi=300)

plt.figure(figsize=(18, 14))
plt.plot(year, ru_year/100000, c='green', alpha=0.8, linewidth=1)
plt.fill_between(year, ru_year/100000-(ru_year/100000).std(),  ru_year/100000+(ru_year/100000).std(), color='lightblue')
plt.title('Russian Boreal Forest ', size=55)
plt.xlabel('Year', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.grid()
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure9.jpeg', format='jpeg', dpi=300)

plt.figure(figsize=(18, 14))
plt.plot(month, ru_month/100000, c='green', alpha=0.8, linewidth=3)
plt.title('Russian Boreal Forest ', size=55)
plt.xlabel('Month', size=55)
plt.ylabel('BA(10^5 hectare)', size=55)
plt.yticks(fontproperties='Times New Roman', size=50)
plt.xticks(fontproperties='Times New Roman', size=50)
plt.grid()
plt.savefig('E:/ModisFire/Graph/raw/burned area/figure10.jpeg', format='jpeg', dpi=300)