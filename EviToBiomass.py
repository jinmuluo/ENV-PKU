from pyhdf.SD import SD, SDC
import numpy as np
import gdal as gl
import find_file as ff
import scipy.optimize as opt
import matplotlib.pyplot as plt
"this python files is writen for regress carbon 2000,  carbon 2006 and monthly Enhanced vegetation index into monthly"
"carbon density or fule load"
" Author: luojinmu "
" Email: myjinmuluo@pku.edu.cn/gmail.com/163.com"
" Time: 2019/2/23"


def cost(para, X, Y):
    var = len(Y)
    Y_pred = np.dot(X, para)
    cost = 1 / var * np.sum(np.power(Y_pred - Y, 2))
    return cost


def gradient(para, X, Y):
    Y_pred = np.dot(X, para)
    gradient = np.dot(X.T, 2 * (Y_pred - Y))
    return gradient

""""
 load the initializing carbon storage data set  [0.01 x 0.01 degree], in this section, you need define the 
 location of your fuel load and clearly point our the format.
 The unit is different , 2000 load it as numpy.array. unit is [C T/hectare]; 2006 are load in unit:
"""
Caddress = 'E:/ModisFire/Carbonstorage/CS-2001.tif'
Carbon = gl.Open(Caddress)
if Carbon == None:
    print('Tiff file is not exits')
im_width = Carbon.RasterXSize
im_height = Carbon.RasterYSize
im_bands = Carbon.RasterCount
carbon = Carbon.ReadAsArray(0, 0, im_width, im_height)
np.nan_to_num(carbon)



"""""
second step: load the Enhanced  data set.
the typical name is: MOD13C1.A2000353.006.2015147154942.hdf
"""""
degree = 0.05
Evi_address = 'G:/MOD13C1(vegetation index)/'
Evi_name_list = ff.find_file(Evi_address)
Evi_long = len(Evi_name_list)

"""
find the year 2001 EVI  to find the relationship about Carbon Storage 2000 and EVI-2001, construct a regression model
"""

evi_2001 = np.zeros([int(180/degree), int(360/degree)])
ndvi_2001 = np.zeros([int(180/degree), int(360/degree)])
count = 0
for i in range(Evi_long):
    if int(Evi_name_list[i][-29:-25]) == 2001:
        f = SD(Evi_name_list[i])
        EVI = f.select('CMG 0.05 Deg 16 days EVI').get()
        NDVI = f.select('CMG 0.05 Deg 16 days NDVI').get()
        evi_2001 = evi_2001 + EVI
        ndvi_2001 = ndvi_2001 + NDVI
        count = count + 1
print('You have ', count, 'Evi flies in Year 2001')

"""
construct the regression model between Carbon 2000 and Evi 2001
"""
order = 5
# change the input data set into vector,fill value is -3000 in MOD13C1 EVI
evi_2001 = np.reshape(evi_2001, [-1, 1])
evi_2001[evi_2001 == -3000] = 0
ndvi_2001 = np.reshape(ndvi_2001, [-1, 1])
carbon = np.reshape(carbon, [-1, 1])
para = np.random.randint(low=0, high=1, size=order)
# because the 0.01 degree is too small, so we need to exclude the sea and ice pixel which carbon density is zero
Y = carbon[evi_2001.nonzero()]
evi_2001 = evi_2001[evi_2001.nonzero()]
evi_2001 = evi_2001[Y.nonzero()]
Y = Y[Y.nonzero()]
# carbon density in Olson map is repeat in regional , so we need to do another resample.
Y = Y[::2000]
evi_2001 = evi_2001[::2000]
print(Y.shape, evi_2001.shape)
plt.scatter(evi_2001, Y)
plt.show()

X = np.zeros([evi_2001.shape[0], order])
for i in range(order):
    X[:, i] = np.power(evi_2001, i)

result = opt.fmin_tnc(func=cost, x0=para, fprime=gradient, args=(X, Y))
print(result[0])
theta = result[0]




