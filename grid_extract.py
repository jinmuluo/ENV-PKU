import numpy as np


"""
NOTE: there are exits two longitude definition, longitude(-180 , 180); longitude(0, 360)
the transfer methods is [-180, 0] = [181, 360]. 
You need to make clear about relationship between your emi_matrix and its longitude definition.
Here we use the definition of [-180, 180]

"""


def extract(grid_x, grid_y, emi, ran):
    grid_x = int(grid_x - ran/2)
    grid_y = int(grid_y - ran/2)
    sum_emi = 0
    for i in range(ran):
        for j in range(ran):
            sum_emi = sum_emi + emi[grid_x + i, grid_y + j]
    return sum_emi
