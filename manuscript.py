from netCDF4 import Dataset
import matplotlib.pyplot as plt
f = Dataset('G:/OMIL32/OMI-Aura_L3-OMSO2e_2004m1003_v003-2018m0531t143408.he5.nc@ColumnAmountSO2_PBL,RadiativeCloudFraction,RelativeAzimuthAngle,SlantColumnAmountSO2,SolarZenithAngle,TerrainHeight,lat,lon')
vcd = f.variables['ColumnAmountSO2_PBL'][:]
term = vcd
plt.imshow(term)
plt.show()