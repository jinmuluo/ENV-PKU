from pyhdf.SD import SD, SDC
import find_file as find
import gdal as gl
import numpy as np
from netCDF4 import Dataset
import ModisTransfer as mt

""""
 load the initializing carbon storage data set  [0.25 degree x 0.25 degree], in this section, you need define the 
 location of your fuel load and clearly point our the format, load it as numpy.array. unit is C T/hectare
"""

Caddress = 'E:/ModisFire/Carbonstorage/CarbonV21.tif'
Carbon = gl.Open(Caddress)
if Carbon == None:
    print('tiff file is not exit')
im_width = Carbon.RasterXSize
im_height = Carbon.RasterYSize
im_bands = Carbon.RasterCount
carbon_term = Carbon.ReadAsArray(0, 0, im_width, im_height)
np.nan_to_num(carbon_term)
carbon_storage = np.zeros([720, 1440])    # our tiff data have some drift, so here are correct it.
carbon_storage[0:718, 0:1439] = carbon_term[3:, 2:]

"""""
In this section,  we load the MODIS Net primary data(NPP) data set [500 meter x 500meter]. finally, you can get a 
namelist of NPP data address and its numbers in variable name_long.
Notice unit is [kg c/m2], and factor is [0.0001]

"""

ModisAddress = 'G:/NPP_GLOBAL/'
ModisNameList = find.find_file(ModisAddress)
name_long = len(ModisNameList[3])

""""
in this section, we load the burned area data [ 0.25 degree x 0.25 degree ], factor is [0.01]
Combustion completeness[percentage/100]; emission factor[ mg / kg dry matter ].
Emission factor are considerate same as all burning type;
Combustion completeness are get form the proved paper, set as [90%] in boreal forest.

"""

ModisBA_address = 'G:/MODIS_Burned_area/C6/'
ModisBANamelist = find.find_file(ModisBA_address)
BAname_long = len(ModisBANamelist[1])
BaP_ef = 9.25*1000  # notice the carbon storage is unit tons, so factor 1000 is use here
PAH16_ef = 70.075*1000
PHE_ef = 48.35*1000
CC = 0.20

"""
Construct the Grid area matrix here

"""

degree = 0.25
area = np.zeros([int(180/degree), int(360/degree)])
area[:] = 111.319554 * degree * 111.319554 * degree
for i in range(area.shape[0]):
    area[i, :] = area[i, :] * np.cos((90 - degree*(i+1))*np.pi/180)
carbon_storage = np.multiply(carbon_storage, area*100)  # transfer the Carbon storage unit: C T/ha into C Tons

"""
Main Code here, repeat form year 2000 to year 2014
result are cluster into NetCDF files, include carbon storage(year); NPP; B[a]P emission(year, total+every burning type).
"""

for i in range(2001, 2015):
    new_name_list = []
    for j in range(len(ModisNameList)):
        term_name = ModisNameList[j][name_long - 46:name_long]
        if int(term_name[10:14]) == i:
            new_name_list.append(ModisNameList[j])
    print('we have', len(new_name_list), 'files in year:', i)
    npp_global_add = mt.modis_transfer(new_name_list, degree=0.25) * 0.0001   # the scale factor is 0.0001
    npp_global_add = np.multiply(npp_global_add/1000, area*1000*1000)     # transfer the unit  kg C/m2 into T-C
    print('Get the NPP data in year:', i)
    exap = SD(ModisBANamelist[1], SDC.READ)
    cover_dist = exap.select('LandCoverDist').get()
    BaP_emission = np.zeros(cover_dist.shape)  # renew the matrix every time
    PAHs_emission = np.zeros(cover_dist.shape)  # renew the matrix every time
    PHE_emission = np.zeros(cover_dist.shape)  # renew the matrix every time
    for j in range(len(ModisBANamelist)):
        ba_term_name = ModisBANamelist[j][BAname_long - 39:BAname_long]
        if int(ba_term_name[10:14]) == i:
            Burned_file = SD(ModisBANamelist[j], SDC.READ)
            burned_area = Burned_file.select('BurnedArea').get() * 0.01  # the scale factor is 0.01, unit is hectare.
            burned_area = np.divide(burned_area, area*100)   # transfer the burned area into percentage in each Grid.
            cover_dist = Burned_file.select('LandCoverDist').get() * 0.01  # fraction of burned area in each land cover class.
            cover_dist[0, :, :] = 1   # use the first type(water) to represent all type emission.

            for k in range(cover_dist.shape[0]):
                BaP_emission[k, :, :] = BaP_emission[k, :, :] + np.multiply(carbon_storage * CC, burned_area)*BaP_ef * cover_dist[k, :, :]
                PHE_emission[k, :, :] = PHE_emission[k, :, :] + np.multiply(carbon_storage * CC, burned_area) * PHE_ef * cover_dist[k, :, :]
                carbon_storage = carbon_storage + npp_global_add/12 - np.multiply(carbon_storage, burned_area)*CC
    yr_hour = 365*24
    for j in range(cover_dist.shape[0]):
        BaP_emission[j, :, :] = np.divide(BaP_emission[j, :, :]/yr_hour, area)
        PAHs_emission[j, :, :] = np.divide(PAHs_emission[j, :, :]/yr_hour, area)
    # create the NetCDF files to storage the result.
    Carbon_storage_name = 'PAH16_emission_' + str(i) + '.nc'
    fire_data = Dataset(Carbon_storage_name, 'w', format='NETCDF4')
    fire_data.description = 'PAHs emission in total and divide into every cover kind(MCD64CMQ), Carbon storage'
    fire_data.createDimension('lat', 720)
    fire_data.createDimension('lon', 1440)
    fire_data.createDimension('type', 16)
    latitude = fire_data.createVariable('latitude', np.float32, ('lat',))
    longitude = fire_data.createVariable('longitude', np.float32, ('lon',))
    fuel_load = fire_data.createVariable('fuel_load', np.float64, ('lat', 'lon',))
    npp = fire_data.createVariable('npp', np.float64, ('lat', 'lon',))
    grid_area = fire_data.createVariable('grid_area', np.float32, ('lat', 'lon',))
    BaP_emi = fire_data.createVariable('BaP_emi', np.float64, ('type', 'lat', 'lon',))
    BaP = fire_data.createVariable('BaP', np.float64, ('lat', 'lon',))
    PHE_emi = fire_data.createVariable('PHE_emi', np.float64, ('type', 'lat', 'lon',))
    PHE = fire_data.createVariable('PHE', np.float64, ('lat', 'lon',))
    PAHs = fire_data.createVariable('PAHs', np.float64, ('lat', 'lon',))
    PAHs_emi = fire_data.createVariable('PAHs_emi', np.float64, ('type', 'lat', 'lon',))
    latitude.unit = 'degree_North in WGS84'
    longitude.unit = 'degree_South in WGS84'
    fuel_load.unit = 'Carbon storage in unit:Carbon Tons'
    npp.unit = 'Net Primary production in unit: Carbon Tons'
    grid_area.unit = ' grid area in unit:km^2'
    BaP_emi.unit = 'B[a]P emission in unit: mg/km2/hr'
    PHE_emi.unit = 'PHR emission in unit: mg/km2/hr'
    PAHs_emi.unit = 'PAHs16 emission in unit: mg/km2/hr'
    fire_data.variables['latitude'][:] = np.arange(90, -90, -0.25)
    fire_data.variables['longitude'][:] = np.arange(-180, 180, 0.25)
    fire_data.variables['fuel_load'][:] = carbon_storage
    fire_data.variables['BaP'][:] = BaP_emission[0, :, :]
    fire_data.variables['BaP_emi'][:] = BaP_emission[1:, :, :]
    fire_data.variables['PHE'][:] = PHE_emission[0, :, :]
    fire_data.variables['PHE_emi'][:] = PHE_emission[1:, :, :]
    fire_data.variables['PAHs'][:] = PAHs_emission[0, :, :]
    fire_data.variables['PAHs_emi'][:] = PAHs_emission[1:, :, :]
    fire_data.variables['npp'][:] = npp_global_add
    fire_data.variables['grid_area'][:] = area
    fire_data.close()
    print('Year', str(i), 'Finished!')



