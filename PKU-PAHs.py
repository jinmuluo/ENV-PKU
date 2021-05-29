import numpy as np
import find_file as find
from datetime import datetime, timedelta
from netCDF4 import Dataset, num2date, date2num


# change the unit g/km2/month  into kg/m2/s
address = 'H:/PKU-FUEL/BaP/'
new_address = 'H:/PKU-FUEL/test/'
namelist = find.find_file(address, '.nc')
time_slice = 12
for name in namelist:
    file = Dataset(name, 'r', format='NETCDF4')
    year = name[-13:-9]
    dates = []
    new_name = new_address + 'BaP_COARDS_' + name[-13:]
    emission = file.variables['emission'][:]
    latitude = file.variables['lat'][:]
    longitude = file.variables['lon'][:]
    new_emission = np.zeros(emission.shape)
    for i in range(emission.shape[0]):
        new_emission[i, :, :] = emission[i, :, :]/1000/1000/1000/(30*24*3600)
        dates.append(datetime(int(year), i+1, 1))
    new_file = Dataset(new_name, 'w', format='NETCDF4_CLASSIC')
    new_file.description = 'PKU-FUEL BaP monthly emission inventory'
    new_file.Title = 'COARDS/netCDF file containing BaP deforestation and wildfire emission data set.'
    new_file.Contact = 'taos@pku.edu.cn, Peking University college of Urban and Environmental Science'
    new_file.Conventions = 'COARDS'
    new_file.createDimension('lon', len(longitude))
    new_file.createDimension('lat', len(latitude))
    new_file.createDimension('time', time_slice)
    lat = new_file.createVariable('lat', np.float32, ('lat',), chunksizes=[len(latitude)])
    lon = new_file.createVariable('lon', np.float32, ('lon',), chunksizes=[len(longitude)])
    PG_SRCE__POPG = new_file.createVariable('PG_SRCE__POPG', np.float32, ('time', 'lat', 'lon',),
                                            chunksizes=[time_slice, len(latitude), len(longitude)])
    time = new_file.createVariable('time', np.int, ('time',), chunksizes=[time_slice])
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
    new_file.variables['PG_SRCE__POPG'][:] = new_emission
    new_file.variables['lat'][:] = latitude
    new_file.variables['lon'][:] = longitude
    new_file.variables['time'][:] = date2num(dates, units=time.units, calendar=time.calendar)
    print(date2num(dates, units=time.units, calendar=time.calendar))
    file.close()
    print(new_name, 'is done!')


