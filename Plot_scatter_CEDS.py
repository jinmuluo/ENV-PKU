import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

CHN_data_address = 'E:/OMI/GRAPH_data/CEDS_VS_SITU/CEDS_CHN_MONTH.txt'
USA_data_address = 'E:/OMI/GRAPH_data/CEDS_VS_SITU/CEDS_USA_MONTH.txt'
EU_data_address = 'E:/OMI/GRAPH_data/CEDS_VS_SITU/CEDS_EU.txt'

CHN_data = pd.read_table(CHN_data_address)
USA_data = pd.read_table(USA_data_address)
EU_data = pd.read_table(EU_data_address)

CHN_situ = np.array(CHN_data.situ)
GC_CHN = np.array(CHN_data.CEDS_CHN)

USA_situ = np.array(USA_data.situ)
GC_USA = np.array(USA_data.CEDS_USA)

EU_situ = np.array(EU_data.situ)
GC_EU = np.array(EU_data.CEDS_EU)

fig, ax = plt.subplots(figsize=(15, 15))
line_x = np.arange(0, 500, 1)
line_y = np.arange(0, 500, 1)
line_y2 = line_y/10
line_y3 = line_y*10
ax.scatter(GC_CHN, CHN_situ, c='cornflowerblue', marker='.', s=200)
ax.plot(line_x, line_y, c='black',  linewidth=1)
ax.plot(line_x, line_y2, c='black', linestyle='-.', linewidth=1)
ax.plot(line_x, line_y3, c='black', linestyle='-.', linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1, 500)
ax.set_ylim(1, 500)
ax.text(50, 3, 'R:', fontsize=25)
ax.text(50, 2, 'P:', fontsize=25)
cor = np.corrcoef(GC_CHN, CHN_situ)
t, p = stats.pearsonr(GC_CHN, CHN_situ)
print(p)
ax.text(70, 3, round(cor[0, 1], 4), fontsize=25)
ax.text(70, 2, '1.1e-10', fontsize=25)
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
ax.scatter(GC_EU, EU_situ, c='cornflowerblue', marker='.', s=200)
ax.plot(line_x, line_y, c='black',  linewidth=1)
ax.plot(line_x, line_y2, c='black', linestyle='-.', linewidth=1)
ax.plot(line_x, line_y3, c='black', linestyle='-.', linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.01, 100)
ax.set_ylim(0.01, 100)
ax.text(3, 0.1, 'R:', fontsize=25)
ax.text(3, 0.05, 'P:', fontsize=25)
cor = np.corrcoef(GC_EU, EU_situ)
t, p = stats.pearsonr(GC_EU, EU_situ)
print(p)
ax.text(5, 0.1, round(cor[0, 1], 4), fontsize=25)
ax.text(5, 0.05, round(p, 4), fontsize=25)
ax.set_xlabel('Simulation μg/m3', size=25)
ax.set_ylabel('Measurement μg/m3', size=25)
ax.set_title('Europe',size=35)
ax.tick_params(labelsize=25)
plt.show()

fig3, ax = plt.subplots(figsize=(15, 15))
line_x = np.arange(0.01, 100, 1)
line_y = np.arange(0.01, 100, 1)
line_y2 = line_y/10
line_y3 = line_y*10
ax.scatter(GC_USA, USA_situ,  c='cornflowerblue', marker='.', s=200)
ax.plot(line_x, line_y, c='black',  linewidth=1)
ax.plot(line_x, line_y2, c='black', linestyle='-.', linewidth=1)
ax.plot(line_x, line_y3, c='black', linestyle='-.', linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.01, 100)
ax.set_ylim(0.01, 100)
ax.text(3, 0.1,  'R:', fontsize=25)
ax.text(3, 0.05,  'P:', fontsize=25)
cor = np.corrcoef(GC_USA, USA_situ)
t, p = stats.pearsonr(GC_USA, USA_situ)
print(p)
ax.text(5, 0.1,  round(cor[0, 1], 4), fontsize=25)
ax.text(5, 0.05, round(p, 4), fontsize=25)
ax.set_xlabel('Simulation μg/m3', size=25)
ax.set_ylabel('Measurement μg/m3', size=25)
ax.set_title('The United States', size=35)
ax.tick_params(labelsize=25)
plt.show()