from netCDF4 import Dataset
import numpy as np
import find_file as find
from datetime import datetime, timedelta
from netCDF4 import Dataset, num2date, date2num


# change the unit h/km2/month  into kg/m2/s
address = 'H:/PKU-FUEL/BaP_wild_fire/'
new_address = 'H:/PKU-FUEL/test/'
namelist = find.find_file(address, '.nc')
for name in namelist:
    file = Dataset(name, 'r', format='NETCDF4')
    year = name[-32:-28]
    dates = []
    new_name = new_address + name[26:]
    emission = file.variables['emission'][:]
    latitude = file.variables['lat'][:]
    longitude = file.variables['lon'][:]
    new_emission = np.zeros(emission.shape)
    for i in range(emission.shape[0]):
        new_emission[i, :, :] = emission[i, :, :]/1000/1000/1000/(30*24*3600)
        dates.append(datetime(int(year), i+1, 1))
    new_file = Dataset(new_name, 'w', format='NETCDF4')
    new_file.description = 'PKU-FUEL PHE monthly emission inventory'
    new_file.createDimension('lon', len(longitude))
    new_file.createDimension('lat', len(latitude))
    new_file.createDimension('time', 12)
    lat = new_file.createVariable('lat', np.float32, ('lat',))
    lon = new_file.createVariable('lon', np.float32, ('lon',))
    BaP = new_file.createVariable('BaP', np.float32, ('time', 'lat', 'lon',))
    time = new_file.createVariable('time', np.int, ('time',))
    lat.units = 'degrees_north'
    lon.units = 'degrees_south'
    BaP.units = 'kg/m2/s'
    time.long_name = 'Time'
    time.calendar = 'standard'
    time.units = 'hours since 1985-01-01 00:00:00'
    new_file.variables['BaP'][:] = new_emission
    new_file.variables['lat'][:] = latitude
    new_file.variables['lon'][:] = longitude
    new_file.variables['time'][:] = date2num(dates, units=time.units, calendar=time.calendar)
    print(date2num(dates, units=time.units, calendar=time.calendar))
    file.close()
    print(new_name, 'is done!')


