import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


CHN_data_address = 'E:/OMI/GRAPH_data/PKU_VS_SITU/CHN_month.txt'
USA_data_address = 'E:/OMI/GRAPH_data/PKU_VS_SITU/USA_month.txt'
EU_data_address = 'E:/OMI/GRAPH_data/PKU_VS_SITU/EU_year.txt'

CHN_data = pd.read_table(CHN_data_address)
USA_data = pd.read_table(USA_data_address)
EU_data = pd.read_table(EU_data_address)

CHN_situ = np.array(CHN_data.situ)
GC_CHN_pku = np.array(CHN_data.GC_PKU)
GC_CHN_omi = np.array(CHN_data.GC_OMI)

USA_situ = np.array(USA_data.situ)
GC_USA_pku = np.array(USA_data.GC_PKU)
GC_USA_omi = np.array(USA_data.GC_OMI)

EU_situ = np.array(EU_data.situ)
GC_EU_pku = np.array(EU_data.GC_PKU)
GC_EU_omi = np.array(EU_data.GC_OMI)

fig, ax = plt.subplots(figsize=(15, 15))
line_x = np.arange(0, 500, 1)
line_y = np.arange(0, 500, 1)
line_y2 = line_y/10
line_y3 = line_y*10
ax.scatter(GC_CHN_pku, CHN_situ, c='slategray', marker='.', s=400)
ax.scatter(GC_CHN_omi, CHN_situ, c='maroon', marker='.', s=100)
label = ['PKU-FUEL', 'PKU-OMI']
ax.legend(label, loc='lower right', shadow=True, fontsize=25)
ax.plot(line_x, line_y, c='black',  linewidth=1)
ax.plot(line_x, line_y2, c='black', linestyle='-.', linewidth=1)
ax.plot(line_x, line_y3, c='black', linestyle='-.', linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1, 500)
ax.set_ylim(1, 500)
ax.text(1.5, 150, 'R:', fontsize=25)
ax.text(1.5, 94, 'P:', fontsize=25)
cor = np.corrcoef(GC_CHN_pku, CHN_situ)
t, p = stats.pearsonr(GC_CHN_pku, CHN_situ)
print(p)
ax.text(2, 150, round(cor[0, 1], 4), color='slategray', fontsize=25)
ax.text(2, 94, '6.3e-07', color='slategray', fontsize=25)
cor = np.corrcoef(GC_CHN_omi, CHN_situ)
t, p = stats.pearsonr(GC_CHN_omi, CHN_situ)
print(p)
ax.text(5, 150, round(cor[0, 1], 4), color='maroon', fontsize=25)
ax.text(5, 94, '3.7e-07', color='maroon', fontsize=25)
ax.set_xlabel('Simulation μg/m3', size=25)
ax.set_ylabel('Measurement μg/m3', size=25)
ax.set_title('China', size=35)
ax.tick_params(labelsize=25)
plt.show()

fig2, ax = plt.subplots(figsize=(15, 15))
line_x = np.arange(0, 500, 1)
line_y = np.arange(0, 500, 1)
line_y2 = line_y/10
line_y3 = line_y*10
ax.scatter(GC_EU_pku, EU_situ, c='slategray', marker='.', s=400)
ax.scatter(GC_EU_omi, EU_situ, c='maroon', marker='.', s=100)
label = ['PKU-FUEL', 'PKU-OMI']
ax.legend(label, loc='lower right', shadow=True, fontsize=25)
ax.plot(line_x, line_y, c='black',  linewidth=1)
ax.plot(line_x, line_y2, c='black', linestyle='-.', linewidth=1)
ax.plot(line_x, line_y3, c='black', linestyle='-.', linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.01, 100)
ax.set_ylim(0.01, 100)
ax.text(0.02, 50, 'R:', fontsize=25)
ax.text(0.02, 20, 'P:', fontsize=25)
cor = np.corrcoef(GC_EU_pku, EU_situ)
t, p = stats.pearsonr(GC_EU_pku, EU_situ)
print(p)
ax.text(0.03, 50, round(cor[0, 1], 4), color='slategray', fontsize=25)
ax.text(0.03, 20, round(p, 4), color='slategray', fontsize=25)
cor = np.corrcoef(GC_EU_omi, EU_situ)
t, p = stats.pearsonr(GC_EU_omi, EU_situ)
print(p)
ax.text(0.1, 50, round(cor[0, 1], 4), color='maroon', fontsize=25)
ax.text(0.1, 20, round(p, 4), color='maroon', fontsize=25)
ax.set_xlabel('Simulation μg/m3', size=25)
ax.set_ylabel('Measurement μg/m3', size=25)
ax.set_title('Europe', size=35)
ax.tick_params(labelsize=25)
plt.show()

fig3, ax = plt.subplots(figsize=(15, 15))
line_x = np.arange(0.01, 100, 1)
line_y = np.arange(0.01, 100, 1)
line_y2 = line_y/10
line_y3 = line_y*10
ax.scatter(GC_USA_pku, USA_situ, c='slategray', marker='.', s=400)
ax.scatter(GC_USA_omi, USA_situ, c='maroon', marker='.', s=100)
label = ['PKU-FUEL', 'PKU-OMI']
ax.legend(label, loc='lower right', shadow=True, fontsize=25)
ax.plot(line_x, line_y, c='black',  linewidth=1)
ax.plot(line_x, line_y2, c='black', linestyle='-.', linewidth=1)
ax.plot(line_x, line_y3, c='black', linestyle='-.', linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.01, 100)
ax.set_ylim(0.01, 100)
ax.text(0.03, 50, 'R:', fontsize=25)
ax.text(0.03, 20, 'P:', fontsize=25)
cor = np.corrcoef(GC_USA_pku, USA_situ)
t, p = stats.pearsonr(GC_USA_pku, USA_situ)
print(p)
ax.text(0.05, 50, round(cor[0, 1], 4), color='slategray', fontsize=25)
ax.text(0.05, 20, '6.4e-12', color='slategray', fontsize=25)
cor = np.corrcoef(GC_USA_omi, USA_situ)
t, p = stats.pearsonr(GC_USA_omi, USA_situ)
print(p)
ax.text(0.15, 50, round(cor[0, 1], 4), color='maroon', fontsize=25)
ax.text(0.15, 20, '8.3e-12', color='maroon', fontsize=25)
ax.set_xlabel('Simulation μg/m3', size=25)
ax.set_ylabel('Measurement μg/m3', size=25)
ax.set_title('The United States', size=35)
ax.tick_params(labelsize=25)
plt.show()