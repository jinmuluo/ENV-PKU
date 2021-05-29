import numpy as np
import find_file as find
from datetime import datetime, timedelta
from netCDF4 import Dataset, num2date, date2num


"""
Goal:In this python file, we gonna add our biomass burning BaP emission sector into PKU-FUEL BaP.
Author: Luo Jinmu
Email: myjinmuluo@pku.edu.cn/163.com
Time:24/06/2019 
"""

# ----------------------------------------------------------------------------------------------------------------------
# Define the data set address and other important parameters.
# ----------------------------------------------------------------------------------------------------------------------
pku_total_address = 'H:/PKU-FUEL/BaP/'
pku_fire_address = 'H:/PKU-FUEL/BaP_wild_fire/'
ljm_fire_address = 'H:/PAHs/v2019-01/'
output_address = 'H:/PAHs/v2019-05/'
suffix = '.nc'
pku_total_namelist = find.find_file(pku_total_address, suffix)
print('Find', len(pku_total_namelist), 'files in address', pku_total_address)
pku_fire_namelist = find.find_file(pku_fire_address, suffix)
print('Find', len(pku_fire_namelist), 'files in address', pku_fire_address)
ljm_fire_namelist = find.find_file(ljm_fire_address, suffix)
print('Find', len(ljm_fire_namelist), 'files in address', ljm_fire_address)


# ----------------------------------------------------------------------------------------------------------------------
# read the data set: because the data set are already in same sequence  and within same year interval
# ----------------------------------------------------------------------------------------------------------------------
for i in range(len(ljm_fire_namelist)):
    pku_total = Dataset(pku_total_namelist[i], 'r', format='NETCDF4')
    pku_fire = Dataset(pku_fire_namelist[i], 'r', format='NETCDF4')
    ljm_fire = Dataset(ljm_fire_namelist[i], 'r', format='NETCDF4')

    # load the data set matrix ,create the output matrix and term matrix
    p_tol = pku_total.variables['emission'][:]
    p_f = pku_fire.variables['emission'][:]
    area1 = pku_total.variables['grid_cell_area'][:]
    ljm = ljm_fire.variables['PG_SRCE__POPG'][:]
    area2 = ljm_fire.variables['grid_area'][:]
    dat = np.zeros(ljm.shape)
    new_tol = np.zeros([p_tol.shape[1], p_tol.shape[2]])
    term1 = np.zeros([p_tol.shape[1], p_tol.shape[2]])
    new_fire = np.zeros([p_tol.shape[1], p_tol.shape[2]])
    term2 = np.zeros([p_tol.shape[1], p_tol.shape[2]])

    # grid and change the map projection of PKU-FUEL matrix in to our need output style
    for j in range(p_tol.shape[0]):
        term1 = term1 + p_tol[j, :, :]
        term2 = term2 + p_f[j, :, :]

    term1 = np.multiply(term1, area1)
    term2 = np.multiply(term2, area1)
    new_tol[:, 0:int(new_tol.shape[1]/2)] = term1[:, int(new_tol.shape[1]/2):]
    new_tol[:, int(new_tol.shape[1] / 2):] = term1[:, 0:int(new_tol.shape[1] / 2)]
    new_fire[:, 0:int(new_tol.shape[1] / 2)] = term2[:, int(new_tol.shape[1] / 2):]
    new_fire[:, int(new_tol.shape[1] / 2):] = term2[:, 0:int(new_tol.shape[1] / 2)]
    for j in range(dat.shape[1]):
        for k in range(dat.shape[2]):
            dat[0, j, k] = sum(sum(new_tol[j*10:(9+j*10), k*10:(9+k*10)] - new_fire[j*10:(9+j*10), k*10:(9+k*10)]))

    dat = dat /1000/(365*24*3600)
    dat = np.divide(dat, area2*1000*1000) + ljm

    # output the matrix in netcdf format.
    year = pku_total_namelist[i][-13:-9]
    name = output_address + 'BaP_improve_' + year + '_1x1' + suffix
    latitude = ljm_fire.variables['lat'][:]
    longitude = ljm_fire.variables['lon'][:]
    new_file = Dataset(name, 'w', format='NETCDF4')
    new_file.description = 'new improve BaP yearly emission inventory'
    new_file.Title = 'COARDS/netCDF file containing BaP all sector emission data set.'
    new_file.Contact = 'myjinmuluo@pku.edu.cn, Peking University college of Urban and Environmental Science'
    new_file.Conventions = 'COARDS'
    new_file.createDimension('lon', len(longitude))
    new_file.createDimension('lat', len(latitude))
    new_file.createDimension('time', 1)
    lat = new_file.createVariable('lat', np.float32, ('lat',), chunksizes=[len(latitude)])
    lon = new_file.createVariable('lon', np.float32, ('lon',), chunksizes=[len(longitude)])
    PG_SRCE__POPG = new_file.createVariable('PG_SRCE__POPG', np.float32, ('time', 'lat', 'lon',),
                                            chunksizes=[1, len(latitude), len(longitude)])
    time = new_file.createVariable('time', np.int, ('time',), chunksizes=[1])
    lat.units = 'degrees_north'
    lat.axis = 'Y'
    lon.units = 'degrees_east'
    lon.axis = 'X'
    PG_SRCE__POPG.units = 'kg/m2/s'
    PG_SRCE__POPG.long_name = 'POPG tracer'
    time.long_name = 'Time'
    time.axis = 'T'
    time.calendar = 'standard'
    time.units = 'hours since 1985-01-01 00:00:00'
    new_file.variables['PG_SRCE__POPG'][:] = dat
    new_file.variables['lat'][:] = latitude
    new_file.variables['lon'][:] = longitude
    new_file.variables['time'][:] = date2num(datetime(int(year), 1, 1, 0), units=time.units, calendar=time.calendar)
    print(date2num(datetime(int(year), 1, 1, 0), units=time.units, calendar=time.calendar))
    pku_total.close()
    pku_fire.close()
    ljm_fire.close()
    new_file.close()
    print(name, 'is done!')







