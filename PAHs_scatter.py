import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tck


# ----------------------------------------------------------------------------------------------------------------------
# Read the data set.
# ----------------------------------------------------------------------------------------------------------------------
data_address = 'E:/ModisFire/GRAPH_DATA/PAHs_year_ave.txt'
file = pd.read_table(data_address)
year = np.array(file.Time)
alert = np.array(file.Alert)
zeppelin = np.array(file.Zeppelin)
pallas = np.array(file.Pallas)
modis_fire_alert = np.array(file.Fire_Alert)
modis_fire_zeppelin = np.array(file.Fire_Zeppelin)
modis_fire_pallas = np.array(file.Fire_Pallas)
modis_total_alert = np.array(file.Total_Alert)
modis_total_zeppelin = np.array(file.Total_Zeppelin)
modis_total_pallas = np.array(file.Total_Pallas)


# ----------------------------------------------------------------------------------------------------------------------
# plot the data set.
# ----------------------------------------------------------------------------------------------------------------------
f2, ax = plt.subplots(figsize=(15, 10))
line_x = np.arange(-10, 700, 1)
line_y = np.arange(-10, 700, 1)
line_y2 = line_y/10
line_y3 = line_y*10
ax.scatter(alert, modis_fire_alert, c='coral', marker='^', s=200, label='alert fire')
ax.scatter(alert, modis_total_alert, c='maroon', marker='^', s=200, label='alert total')
ax.scatter(zeppelin, modis_fire_zeppelin, c='lime', marker='o', s=200, label='zeppelin fire')
ax.scatter(zeppelin, modis_total_zeppelin, c='dodgerblue', marker='o', s=200, label='zeppelin total')
ax.scatter(pallas, modis_fire_pallas, c='crimson', marker='x', s=200, label='pallas fire')
ax.scatter(pallas, modis_total_pallas, c='darkmagenta', marker='x', s=200, label='pallas total')
ax.plot(line_x, line_y, c='black',  linewidth=1)
ax.plot(line_x, line_y2, c='black', linestyle='-.', linewidth=1)
ax.plot(line_x, line_y3, c='black', linestyle='-.', linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.1, 500)
ax.set_ylim(0.1, 500)
ax.set_ylabel('Simulation(pg/m³)', size=25)
ax.set_xlabel('Measured(pg/m³)', size=25)
ax.tick_params(labelsize=25)
ax.legend(loc='upper left', shadow=True, fontsize=20)
plt.show()