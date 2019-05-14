import numpy as np
import gdal
import find_file as find
from netCDF4 import Dataset


"""
This python file is writen for transfer the Biomass(carbon density) tiff data into hdf files
author: Luo Jinmu
Email: myjinmuluo@pku.edu.cn/gmail.com/163.com
time: 2019/2/28 
"""

" First step:input the real carbon storage map(Unit: tonnes). "
degree = 0.05
row = int(180/degree)
col = int(360/degree)
Address = 'E:/ModisFire/Biomass/FRA+Pan/'
Tiff_address = find.find_file(Address, '.tif')
Biomass = np.zeros([row, col, len(Tiff_address)])
for i in range(len(Tiff_address)):
    Carbon = gdal.Open(Tiff_address[i])
    if Carbon is None:
        print('Tiff file is not exits')
    im_width = Carbon.RasterXSize
    im_height = Carbon.RasterYSize
    im_bands = Carbon.RasterCount
    Biomass[-im_height:, :, i] = Carbon.ReadAsArray(0, 0, im_width, im_height)
    np.nan_to_num(Biomass)

"Second step: Load the NPP data"
npp_address = 'G:/NPP_yearly/0.05 deg/'
npp_namelist = find.find_file(npp_address, '.nc')
print('load the ', len(npp_namelist), 'NPP')
npp = np.zeros([row, col, len(npp_namelist)])
for i in range(len(npp_namelist)):
    f = Dataset(npp_namelist[i], 'r', format='NETCDF4')
    npp[:, :, i] = f.variables['npp'][:]

" Construct the area matrix in unit hectare"
area = np.zeros([row, col])
for i in range(row):
    area[i, :] = np.cos((90 - degree/2 - i*degree)*np.pi/180)*111.31*111.31*degree*degree * 100
print('Construct the area map done!')

"Construct the yearly continuous Biomass 1990-2016"
new_biomass = np.zeros([Biomass.shape[0], Biomass.shape[1], 2016-1990])
new_biomass[:, :, 0] = Biomass[:, :, 0]
new_biomass[:, :, 10] = Biomass[:, :, 1] + npp[:, :, 0]
new_biomass[:, :, 15] = Biomass[:, :, 2] + npp[:, :, 4]
new_biomass[:, :, 20] = Biomass[:, :, 3] + npp[:, :, 9]
new_biomass[:, :, 25] = Biomass[:, :, 4] + npp[:, :, 14]
for i in range(1, 10):
    new_biomass[:, :, i] = Biomass[:, :, 0] + (Biomass[:, :, 1] - Biomass[:, :, 0]) / 10
for i in range(11, 15):
    new_biomass[:, :, i] = Biomass[:, :, 1] + (Biomass[:, :, 2] - Biomass[:, :, 1]) / 5 + npp[:, :, i-11]
for i in range(16, 20):
    new_biomass[:, :, i] = Biomass[:, :, 2] + (Biomass[:, :, 3] - Biomass[:, :, 2]) / 5 + npp[:, :, i-11]
for i in range(21, 25):
    new_biomass[:, :, i] = Biomass[:, :, 3] + (Biomass[:, :, 4] - Biomass[:, :, 3]) / 5 + npp[:, :, i-11]
for i in range(new_biomass.shape[2]):
    new_biomass[:, :, i] = np.divide(new_biomass[:, :, i], area)
print('Calculate the biomass done!')

" out put the biomass series 1990-2016"
for i in range(1990, 2016):
    Biomass_name = 'Living Biomass' + str(i) + '.nc'
    Biomass_f = Dataset(Biomass_name, 'w', format='NETCDF4')
    Biomass_f.createDimension('lat', row)
    Biomass_f.createDimension('lon', col)
    latitude = Biomass_f.createVariable('latitude', np.float32, ('lat',))
    longitude = Biomass_f.createVariable('longitude', np.float32, ('lon',))
    Living_Biomass = Biomass_f.createVariable('Living_Biomass', np.float32, ('lat', 'lon',))
    latitude.unit = 'degree_North in WGS84 Coordination system'
    longitude.unit = 'degree_South in WGS84 Coordination system'
    Living_Biomass.unit = 'Living Biomass in unit: tonnes/hectare'
    Biomass_f.variables['latitude'][:] = np.arange(90, -90, -degree)
    Biomass_f.variables['longitude'][:] = np.arange(-180, 180, degree)
    Biomass_f.variables['Living_Biomass'][:] = new_biomass[:, :, i-1990]
    print('Year', str(i), 'Finished!')





















