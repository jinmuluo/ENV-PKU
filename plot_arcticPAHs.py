import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from datetime import datetime
import matplotlib.dates as mdates

# ----------------------------------------------------------------------------------------------------------------------
# Read the data set.
# ----------------------------------------------------------------------------------------------------------------------
data_address = 'E:/ModisFire/GRAPH_DATA/geoschem2.txt'
data_address2 = 'E:/ModisFire/GRAPH_DATA/fire_contribution.txt'
data_address3 = 'E:/ModisFire/GRAPH_DATA/PAHs_minus.txt'
file = pd.read_table(data_address)
file2 = pd.read_table(data_address2)
file3 = pd.read_table(data_address3)
year = np.array(file.Time)
alert = np.array(file.Alert)
zeppelin = np.array(file.Zeppelin)
pallas = np.array(file.Pallas)
modis_fire_alert = np.array(file.modis_fire_alert)
modis_fire_zeppelin = np.array(file.modis_fire_zeppelin)
modis_fire_pallas = np.array(file.modis_fire_pallas)
modis_total_alert = np.array(file.modis_alert)
modis_total_zeppelin = np.array(file.modis_zeppelin)
modis_total_pallas = np.array(file.modis_pallas)
alert_c = np.array(file2.alert_c)
zeppelin_c = np.array(file2.zeppelin_c)
pallas_c = np.array(file2.pallas_c)
alert_m = np.array(file3.alert_m)
zeppelin_m = np.array(file3.zeppelin_m)
pallas_m = np.array(file3.pallas_m)
time = range(len(year))
# ----------------------------------------------------------------------------------------------------------------------
# Plot the graphs
# ----------------------------------------------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(36, 18))
time = [datetime.strptime(d, "%Y/%m/%d") for d in year]
ax.plot(time, alert, c='seagreen', alpha=1, linewidth=5)
ax.plot(time, modis_fire_alert, c='darkviolet', alpha=1, linewidth=5)
ax.plot(time, modis_total_alert, c='goldenrod', alpha=1, linewidth=5)
ax.legend(('Measured', 'Wild fire', 'Total sector'), fontsize=50)
ax.set_ylabel('BaP(Pg/m³)', fontsize=60)
ax.tick_params(labelsize=55)
plt.savefig('E:/ModisFire/Graph/raw/PAH concentration/figure1.jpeg', format='jpeg', dpi=300)

fig2, ax = plt.subplots(figsize=(36, 18))
ax.plot(time, zeppelin, c='seagreen', alpha=1, linewidth=5)
ax.plot(time, modis_fire_zeppelin, c='darkviolet', alpha=1, linewidth=5)
ax.plot(time, modis_total_zeppelin, c='goldenrod', alpha=1, linewidth=5)
ax.legend(('Measured', 'Wild fire', 'Total sector'), fontsize=50)
ax.set_ylabel('BaP(Pg/ m³)', fontsize=60)
ax.tick_params(labelsize=55)
# ax.set_xticklabels(year, fontdict=font)
plt.savefig('E:/ModisFire/Graph/raw/PAH concentration/figure2.jpeg', format='jpeg', dpi=300)

fig3, ax = plt.subplots(figsize=(36, 18))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.plot(time, pallas, c='seagreen', alpha=1, linewidth=5)
ax.plot(time, modis_fire_pallas, c='darkviolet', alpha=1, linewidth=5)
ax.plot(time, modis_total_pallas, c='goldenrod', alpha=1, linewidth=5)
ax.legend(('Measured', 'Wild fire', 'Total sector'), fontsize=50)
ax.set_xlabel('Year', fontsize=60)
ax.set_ylabel('BaP(Pg/m³)', fontsize=60)
ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=12))
ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
ax.tick_params(labelsize=55)
plt.savefig('E:/ModisFire/Graph/raw/PAH concentration/figure3.jpeg', format='jpeg', dpi=300)

fig4, ax = plt.subplots(figsize=(36, 18))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.plot(time, alert_c*100, c='crimson', alpha=1, linewidth=5)
ax.plot(time, zeppelin_c*100, c='navy', alpha=1, linewidth=5)
ax.plot(time, pallas_c*100, c='yellowgreen', alpha=1, linewidth=5)
ax.legend(('Alert', 'Zeppelin', 'Pallas'), fontsize=50)
ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=12))
ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
ax.set_xlabel('Year', fontsize=60)
ax.set_ylabel('Contribution(%)', fontsize=60)
ax.tick_params(labelsize=55)
plt.savefig('E:/ModisFire/Graph/raw/PAH concentration/figure4.jpeg', format='jpeg', dpi=300)

fig5, ax = plt.subplots(figsize=(36, 18))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.plot(time, alert_m, c='crimson', alpha=0.8, linewidth=3)
ax.plot(time, zeppelin_m, c='navy', alpha=0.8, linewidth=3)
ax.plot(time, pallas_m, c='yellowgreen', alpha=0.8, linewidth=3)
ax.legend(('Alert', 'Zeppelin', 'Pallas'), fontsize=60)
ax.set_title('Total Sector - Wild Fire', fontsize=60)
ax.set_xlabel('Time', fontsize=60)
ax.set_ylabel('BaP, Pg/m³', fontsize=60)
ax.tick_params(labelsize=55)
plt.savefig('E:/ModisFire/Graph/raw/PAH concentration/figure5.jpeg', format='jpeg', dpi=300)

