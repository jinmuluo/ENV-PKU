from pyhdf.SD import SD, SDC
import numpy as np


def modis_transfer(address, degree):
    # Define some important MODIS orbit parameter, unit is meter.
    R = 6371007.181
    T = 1111950
    x_min = -20015109
    y_max = 10007555
    w = 463.31271653
    name_long = len(address)
    npp_global = np.zeros([int(180/degree), int(360/degree)])
    count = np.zeros([int(180/degree), int(360/degree)])
    for i in range(name_long):
        # read the HDF files
        f = SD(address[i], SDC.READ)
        npp_500m = f.select('Npp_500m').get()
        npp_500m[npp_500m > 32760] = 0
        npp_QC_500m = f.select('Npp_QC_500m').get()

        # transfer the NPP into degree map.
        modis_name = address[i][len(address[i])-46:len(address[i])]
        H = int(modis_name[19:21])
        V = int(modis_name[22:24])
        print('horizontal:', H, 'Vertical:', V)
        lat = np.zeros(npp_500m.shape)
        lon = np.zeros(npp_500m.shape)
        for_i = np.arange(0.5, 2400, 1.0)
        for_j = np.arange(0.5, 2400, 1.0)
        x = for_i * w + H * T + x_min
        y = y_max - for_j * w - V * T
        for l in range(lat.shape[0]):
            lat[:, l] = y/R
        for l in range(lon.shape[0]):
            lon[l, :] = np.around(x / (R * np.cos(lat[l, :])) * 180 / np.pi, decimals=4)
        lat = np.around(lat * 180 / np.pi, decimals=4)
        for k in range(2400):
            for j in range(2400):
                if lon[k, j] >= 180-degree or lon[k, j] <= -180+degree or lat[k, j] <= -90+degree or lat[k, j] >= 90-degree:
                    continue
                grid_x = 180 / degree + np.round(lon[k, j] / degree, decimals=2)
                grid_y = 90 / degree - np.round(lat[k, j] / degree, decimals=2)
                npp_global[int(grid_y), int(grid_x)] = npp_global[int(grid_y), int(grid_x)] + npp_500m[k, j]
                count[int(grid_y), int(grid_x)] = count[int(grid_y), int(grid_x)] + 1
    count[np.where(count == 0)] = 1
    npp_global = np.divide(npp_global, count)
    return npp_global

