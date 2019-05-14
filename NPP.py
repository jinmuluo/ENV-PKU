import find_file as find
import numpy as np
from netCDF4 import Dataset
import ModisTransfer as mt


"""""
In this section,  we load the MODIS Net primary data(NPP) data set [500 meter x 500meter]. finally, you can get a 
namelist of NPP data address and its numbers in variable name_long.
Notice unit is [kg c/m2], and factor is [0.0001]

"""
# two parameter need to be define.
Modis_Address = 'G:/MOD17A3H(net primary production)/'
degree = 0.05

ModisNameList = find.find_file(Modis_Address, '.hdf')
name_long = len(ModisNameList[1])
for i in range(2002, 2015):
    new_name_list = []
    for j in range(len(ModisNameList)):
        term_name = ModisNameList[j][name_long - 46:name_long]
        if int(term_name[10:14]) == i:
            new_name_list.append(ModisNameList[j])
    print('we have', len(new_name_list), 'files in year:', i)
    npp_global_add = mt.modis_transfer(new_name_list, degree=0.05) * 0.0001   # the scale factor is 0.0001
    print('Get the NPP data in year:', i)
    # create the NetCDF files to storage the result.
    NPP_name = 'Modis_NPP_' + str(i) + '.nc'
    npp_data = Dataset(NPP_name, 'w', format='NETCDF4')
    npp_data.description = 'Net Primary Productivity (MOD17A3H), Carbon storage'
    npp_data.createDimension('lat', int(180/degree))
    npp_data.createDimension('lon', int(360/degree))
    npp_data.createDimension('type', 16)
    latitude = npp_data.createVariable('latitude', np.float32, ('lat',))
    longitude = npp_data.createVariable('longitude', np.float32, ('lon',))
    npp = npp_data.createVariable('npp', np.float64, ('lat', 'lon',))
    latitude.unit = 'degree_North in WGS84'
    longitude.unit = 'degree_South in WGS84'
    npp.unit = 'Net Primary production in unit: Kg C /m^2(none scale factor)'
    npp_data.variables['latitude'][:] = np.arange(90, -90, -degree)
    npp_data.variables['longitude'][:] = np.arange(-180, 180, degree)
    npp_data.variables['npp'][:] = npp_global_add
    npp_data.close()
    print('Year', str(i), 'Finished!')