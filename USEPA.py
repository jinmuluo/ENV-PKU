import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


data = pd.read_table('E:/OMI/GRAPH_data/usepa.txt')
pku = np.array(data.pku)
edgar = np.array(data.edgar)
ceds = np.array(data.ceds)
eclipse = np.array(data.eclipse)
omi = np.array(data.omi)
omi_htap = np.array(data.htap)
pkuomi = np.array(data.pkuomi)
usepa = np.array(data.usepa)

fig, ax = plt.subplots(figsize=(15, 15))
line_x = np.arange(0, 1500, 1)
line_y = np.arange(0, 1500, 1)
line_y2 = line_y/10
line_y3 = line_y*10
ax.scatter(usepa, pku, c='maroon', marker='x', s=400)
ax.scatter(usepa, pkuomi, c='green', marker='+', s=400)
ax.scatter(usepa, ceds, c='cornflowerblue', marker='.', s=200)
label = ['PKU-FUEL', 'PKU-OMI', 'CEDS']
ax.legend(label, loc='lower right', shadow=True, fontsize=25)
ax.plot(line_x, line_y, c='black',  linewidth=1)
ax.plot(line_x, line_y2, c='black', linestyle='-.', linewidth=1)
ax.plot(line_x, line_y3, c='black', linestyle='-.', linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(5, 1000)
ax.set_ylim(5, 1000)
ax.text(10, 700, 'R:', fontsize=25)
ax.text(10, 504, 'P:', fontsize=25)
cor = np.corrcoef(usepa, pku)
t, p = stats.pearsonr(usepa, pku)
ax.text(12, 700, round(cor[0, 1], 4), color='maroon', fontsize=25)
print(p)
ax.text(12, 504, round(p, 4), color='maroon', fontsize=25)
cor = np.corrcoef(usepa, pkuomi)
t, p = stats.pearsonr(usepa, pkuomi)
print(p)
ax.text(25, 700, round(cor[0, 1], 4), color='green', fontsize=25)
ax.text(25, 504, '9.3e-07', color='green', fontsize=25)

cor = np.corrcoef(usepa, ceds)
t, p = stats.pearsonr(usepa, ceds)
print(p)
ax.text(50, 700, round(cor[0, 1], 4), color='cornflowerblue', fontsize=25)
ax.text(50, 504, round(p, 4), color='cornflowerblue', fontsize=25)

ax.set_xlabel('Measurement, Kt/yr ', size=35)
ax.set_ylabel('Inventory, Kt/yr', size=35)
ax.tick_params(labelsize=25)
plt.show()


