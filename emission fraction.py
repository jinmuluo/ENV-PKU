import numpy as np
from netCDF4 import Dataset
import h5py


pku_address = 'E:/SO2_2010_total.nc'
edgar_address = 'G:/EDGAR_SO2_1970-2012/v432_SO2_2010.0.1x0.1.nc'
ceds_address = 'G:/CEDS/SO2-em-anthro_CMIP_CEDS_2010.nc'
eclipse_address = 'G:/Eclipse/ECLIPSE_base_CLE_V5a_SO2.nc'
omihtap_address = 'G:/OMI-HTAP/v2019-01/htapv2.2.emisso2.surface.x3600y1800t12.2010.integrate.nc4'
omihtap2_address = 'G:/OMI-HTAP/v2019-01/htapv2.2.emisso2.elevate.x3600y1800t12.2010.integrate.nc4'
degree = 0.5
row = int(180/degree)
col = int(360/degree)
pku_emi = np.zeros([row, col])
edgar_emi = np.zeros([row, col])
ceds_emi = np.zeros([row, col])
eclipse_emi = np.zeros([row, col])
omihtap_emi = np.zeros([row, col])
area = np.zeros([row, col])
for i in range(area.shape[0]):
    area[i, :] = 111.31 * degree * 111.31 * degree * np.cos((90 - degree / 2 - i * degree) * np.pi / 180)

pku_f = Dataset(pku_address, 'r', format='NETCDF4')
pku_term = pku_f.variables['emission'][:]
sh = row, pku_term.shape[1] // row, col, pku_term.shape[2] // col
for i in range(pku_term.shape[0]):
    term = np.multiply(pku_term[i, :, :].reshape(sh).mean(axis=3).mean(1), area)/1000/1000/1000
    pku_emi = pku_emi + term
term = pku_emi
pku_new = np.zeros(pku_emi.shape)
pku_new[:, 0:int(col/2)] = term[:, int(col/2):]
pku_new[:, int(col/2):] = term[:, 0:int(col/2)]

edgar_f = Dataset(edgar_address, 'r', format='NETCDF4')
edgar_term = edgar_f.variables['emi_so2'][:]
edgar_emi = np.multiply(edgar_term.reshape(sh).mean(axis=3).mean(1), area*1000*1000)*366*24*3600/1000/1000
term = edgar_emi
edgar_new = np.zeros(edgar_emi.shape)
edgar_new[:, 0:int(col/2)] = term[:, int(col/2):]
edgar_new[:, int(col/2):] = term[:, 0:int(col/2)]

ceds_f = Dataset(ceds_address, 'r', format='NETCDF4')
emission1 = ceds_f.variables['SO2_agr'][:]
emission2 = ceds_f.variables['SO2_ene'][:]
emission3 = ceds_f.variables['SO2_ind'][:]
emission4 = ceds_f.variables['SO2_rco'][:]
emission5 = ceds_f.variables['SO2_shp'][:]
emission6 = ceds_f.variables['SO2_slv'][:]
emission7 = ceds_f.variables['SO2_tra'][:]
emission8 = ceds_f.variables['SO2_wst'][:]
ceds_term = emission1 + emission2 + emission3 + emission4 + emission5 + emission6 + emission7 + emission8
for i in range(ceds_term.shape[0]):
    ceds_emi = ceds_emi + np.multiply(ceds_term[i, :, :], area*1000*1000)*30*24*3600/1000/1000

eclipse_f = Dataset(eclipse_address, 'r', format='NETCDF4')
eclipse_term = eclipse_f.variables['emis_all']
eclipse_emi = eclipse_term[4, :, :]

omihtap_f = Dataset(omihtap_address, 'r', format='NETCDF4')
omihtap_f2 = Dataset(omihtap2_address, 'r', format='NETCDF4')
omihtap_term = omihtap_f.variables['sanl1']
omihtap_term2 = omihtap_f2.variables['sanl2']
for i in range(omihtap_term.shape[0]):
    term = np.multiply(omihtap_term[i, :, :].reshape(sh).mean(axis=3).mean(1), area*1000*1000)*30*24*3600/1000/1000
    term2 = np.multiply(omihtap_term[i, :, :].reshape(sh).mean(axis=3).mean(1), area * 1000 * 1000) * 30 * 24 * 3600 / 1000 / 1000
    omihtap_emi = omihtap_emi + term + term2

p_e = np.divide((pku_new - edgar_new), edgar_new+0.0001)
p_c = np.divide((pku_new - ceds_emi), ceds_emi+0.0001)
p_ec = np.divide((pku_new - eclipse_emi), eclipse_emi+0.0001)
p_ot = np.divide((pku_new - omihtap_emi), omihtap_emi+0.0001)
omi_p = np.divide((omihtap_emi - pku_new), pku_new+0.0001)
omi_e = np.divide((omihtap_emi - edgar_new), edgar_new+0.0001)
omi_c = np.divide((omihtap_emi - ceds_emi), ceds_emi+0.0001)
omi_ec = np.divide((omihtap_emi - eclipse_emi), eclipse_emi+0.0001)

file_name = 'graph.hdf'
file_hdf = h5py.File(file_name, 'w')
# pku = file_hdf.create_dataset('pku', pku_emi.shape, data=pku_new)
# edgar = file_hdf.create_dataset('edgar', edgar_emi.shape, data=edgar_new)
# ceds = file_hdf.create_dataset('ceds', ceds_emi.shape, data=ceds_emi)
# eclipse = file_hdf.create_dataset('eclipse', eclipse_emi.shape, data=eclipse_emi)
pku_edgar = file_hdf.create_dataset('(pku-edgar)', edgar_emi.shape, data=p_e)
pku_ceds = file_hdf.create_dataset('(pku-ceds)', ceds_emi.shape, data=p_c)
pku_eclipse = file_hdf.create_dataset('(pku-eclipse)', eclipse_emi.shape, data=p_ec)
pku_omihtap = file_hdf.create_dataset('(pku-omihtap)', omihtap_emi.shape, data=p_ot)
omihtap_pkus = file_hdf.create_dataset('(omihtap-pku)', ceds_emi.shape, data=omi_p)
omihtap_edgar = file_hdf.create_dataset('(omihtap-edgar)', edgar_new.shape, data=omi_e)
omihtap_ceds = file_hdf.create_dataset('(omihtap-ceds)', ceds_emi.shape, data=omi_c)
omihtap_eclipse = file_hdf.create_dataset('(omihtap-eclipse)', eclipse_emi.shape, data=omi_ec)
lat = file_hdf.create_dataset('lat', data=np.arange(-90+degree/2, 90+degree/2, degree))
lon = file_hdf.create_dataset('lon', data=np.arange(-180+degree/2, 180+degree/2, degree))

latitude = np.arange(-90+degree/2, 90+degree/2, degree)
longitude = np.arange(-180+degree/2, 180+degree/2, degree)
data = np.zeros([row*col, 10])
count = 0
for i in range(row):
    for j in range(col):
        data[count, 0] = latitude[i]
        data[count, 1] = longitude[j]
        data[count, 2] = p_e[i, j]
        data[count, 3] = p_c[i, j]
        data[count, 4] = p_ec[i, j]
        data[count, 5] = p_ot[i, j]
        data[count, 6] = omi_p[i, j]
        data[count, 7] = omi_e[i, j]
        data[count, 8] = omi_c[i, j]
        data[count, 9] = omi_ec[i, j]
        count=count+1
np.savetxt('graph.txt', data)



