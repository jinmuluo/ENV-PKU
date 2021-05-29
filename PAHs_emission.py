import find_file as find
from pyhdf.SD import SD, SDC
import numpy as np
from netCDF4 import Dataset

""""
Load the Living Biomass 2000 - 2015, unit in [tonnes/hectare], 0.05 deg
Typical name is 'Living Biomass1990.nc'
"""
Living_Address = 'H:/Living Biomass/'
Living_namelist = find.find_file(Living_Address, '.nc')
print('load', len(Living_namelist), 'Living Biomass files.')

"""
Load the Modis Burned area data set, unit in [hectare],  0.25 deg, scale factor 0.01
Typical name: 'MCD64CMQ.A2000306.006.2018149224217.hdf'
"""

ModisBA_address = 'H:/MCD64CMQ(burned area)/C6/'
ModisBANamelist = find.find_file(ModisBA_address, '.hdf')
BAname_long = len(ModisBANamelist[1])
print('load', len(ModisBANamelist), 'Burned Area data set.')

"""
define the emission factor, Combustion factor
"""
# notice the carbon storage in unit tons, and the emission factor is always in [mg/kg]
# transfer its into [mg/tonnes],  so factor 1000 is use here
BaP_ef = 1*1000
PHE_ef = 8*1000
CC = 0.20
degree = 0.25
row = int(180/degree)
col = int(360/degree)

"""
Construct the Grid area matrix here, in unit [km2]
"""
area = np.zeros([row, col])
area[:] = 111.319554 * degree * 111.319554 * degree
for i in range(area.shape[0]):
    area[i, :] = area[i, :] * np.cos((90 - degree/2 - degree * i)*np.pi/180)


"""
Main Code here, repeat form year 2001 to year 2014
result are cluster into NetCDF files, include carbon storage(year); NPP; B[a]P emission(year, total+every burning type).

"""
# ----------------------------------------------------------------------------------------------------------------------
# begin to calculate the emission.
# ----------------------------------------------------------------------------------------------------------------------
example = SD(ModisBANamelist[1], SDC.READ)
cover_dist = example.select('LandCoverDist').get()
for i in range(2001, 2015):
    # renew the pollution matrix every year.
    BaP_emission = np.zeros(cover_dist.shape)
    PAHs_emission = np.zeros(cover_dist.shape)
    PHE_emission = np.zeros(cover_dist.shape)
    # load the corresponding Living Biomass in year i
    for k in range(len(Living_namelist)):
        if int(Living_namelist[k][-7:-3]) == i:
            f = Dataset(Living_namelist[k], 'r', format='NETCDF4')
            carbon_storage = f.variables['Living_Biomass'][:]
            sh = row, carbon_storage.shape[0]//row, col, carbon_storage.shape[1]//col
            carbon_storage = carbon_storage.reshape(sh).mean(3).mean(1)
            carbon_storage = np.multiply(carbon_storage, area*100)

    # load the Burned Area data in year i, and calculate the emission year i
    for j in range(len(ModisBANamelist)):
        ba_term_name = ModisBANamelist[j][BAname_long - 39:BAname_long]
        if int(ba_term_name[10:14]) == i:
            Burned_file = SD(ModisBANamelist[j], SDC.READ)
            burned_area = Burned_file.select('BurnedArea').get() * 0.01  # the scale factor is 0.01, unit is hectare.
            burned_area = np.divide(burned_area, area*100)   # transfer the burned area into percentage in each Grid.
            cover_dist = Burned_file.select('LandCoverDist').get() * 0.01  # fraction of burned area in each land class.
            cover_dist[0, :, :] = 1   # use the first type(water) to represent all type emission.

            for k in range(cover_dist.shape[0]):
                BaP_emission[k, :, :] = BaP_emission[k, :, :] + np.multiply(carbon_storage * CC,
                                                                            burned_area)*BaP_ef * cover_dist[k, :, :]
                PHE_emission[k, :, :] = PHE_emission[k, :, :] + np.multiply(carbon_storage * CC,
                                                                            burned_area) * PHE_ef * cover_dist[k, :, :]


# ----------------------------------------------------------------------------------------------------------------------
# unit transfer, mg/yr in every grid --> kg/m2/s,  and upside down the matrix
# ----------------------------------------------------------------------------------------------------------------------
    yr_second = 365*24*3600
    mg_to_kg = 1000*1000
    km2_to_m2 = 1000*1000
    for j in range(cover_dist.shape[0]):
        BaP_emission[j, :, :] = np.divide(BaP_emission[j, :, :]/yr_second/mg_to_kg, area*km2_to_m2)
        term = BaP_emission[j, :, :]
        BaP_emission[j, :, :] = term[::-1]
        PHE_emission[j, :, :] = np.divide(PHE_emission[j, :, :]/yr_second/mg_to_kg, area*km2_to_m2)
        term = PHE_emission[j, :, :]
        PHE_emission[j, :, :] = term[::-1]


# ----------------------------------------------------------------------------------------------------------------------
# create the NetCDF files to storage the result.
# ----------------------------------------------------------------------------------------------------------------------
    Carbon_storage_name = 'PAHs_emission_' + str(i) + '.nc'
    fire_data = Dataset(Carbon_storage_name, 'w', format='NETCDF4')
    fire_data.description = 'PAHs emission in total and divide into every cover kind(MCD64CMQ), Carbon storage'
    latitude = fire_data.createDimension('latitude', row)
    longitude = fire_data.createDimension('longitude', col)
    type = fire_data.createDimension('type', 16)
    lat = fire_data.createVariable('lat', np.float32, ('latitude',))
    lon = fire_data.createVariable('lon', np.float32, ('longitude',))
    fuel_load = fire_data.createVariable('fuel_load', np.float64, ('latitude', 'longitude',))
    grid_area = fire_data.createVariable('grid_area', np.float32, ('latitude', 'longitude',))
    BaP_emi = fire_data.createVariable('BaP_emi', np.float64, ('type', 'latitude', 'longitude',))
    BaP = fire_data.createVariable('BaP', np.float64, ('latitude', 'longitude',))
    PHE_emi = fire_data.createVariable('PHE_emi', np.float64, ('type', 'latitude', 'longitude',))
    PHE = fire_data.createVariable('PHE', np.float64, ('latitude', 'longitude',))
    lat.units = 'degrees_north'
    lat.axis = 'Y'
    lon.units = 'degrees_east'
    lon.axis = 'X'
    fuel_load.units = 'ton'
    grid_area.units = 'km2'
    BaP_emi.units = 'kg/m2/s'
    PHE_emi.units = 'kg/m2/s'
    fire_data.variables['lat'][:] = np.arange(-90+(degree/2), 90+(degree/2), degree)
    fire_data.variables['lon'][:] = np.arange(-180+(degree/2), 180+(degree/2), degree)
    fire_data.variables['fuel_load'][:] = carbon_storage[::-1]
    fire_data.variables['BaP'][:] = BaP_emission[0, :, :]
    fire_data.variables['BaP_emi'][:] = BaP_emission[1:, :, :]
    fire_data.variables['PHE'][:] = PHE_emission[0, :, :]
    fire_data.variables['PHE_emi'][:] = PHE_emission[1:, :, :]
    fire_data.variables['grid_area'][:] = area
    fire_data.close()
    print('Year', str(i), 'Finished!')
