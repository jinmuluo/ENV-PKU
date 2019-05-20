import numpy as np
"""
Note! the incoming global matrix must be lat[-90, 90], lon[-180, 180]
"""


def region_ext(emi_matrix, degree):
    row = int(180/degree)
    col = int(360/degree)
    americas_up = int(row/2 + (66 / degree))
    americas_down = int(row/2 - (60 / degree))
    americas_left = int( col/2 - (165 / degree))
    americas_right = int(col/2 - (34 / degree))

    africa_up = int(row / 2 + 36 / degree)
    africa_down = int(row / 2 - 36 / degree)
    africa_left = int(col / 2 - 18 / degree)
    africa_right = int(col / 2 + 43 / degree)

    europe_up = int(row / 2 + 90 / degree)
    europe_down = int(row / 2 + 36 / degree)
    europe_left = int(col / 2 - 20 / degree)
    europe_right = int(col / 2 + 65 / degree)

    asia_up = int(row / 2 + 50 / degree)
    asia_down = int(row / 2 - 10 / degree)
    asia_left = int(col / 2 + 40 / degree)
    asia_right = int(col / 2 + 148 / degree)

    oceania_up = int(row / 2 - 10 / degree)
    oceania_down = int(row / 2 - 50 / degree)
    oceania_left = int(col / 2 + 108 / degree)
    oceania_right = int(col / 2 + 180 / degree)

    china_up = int(row / 2 + 50 / degree)
    china_down = int(row / 2 + 15 / degree)
    china_left = int(col / 2 + 92 / degree)
    china_right = int(col / 2 + 128 / degree)

    americas = sum(sum(emi_matrix[americas_down:(americas_up+1), americas_left:(americas_right+1)]))
    africa = sum(sum(emi_matrix[africa_down:(africa_up + 1), africa_left:(africa_right + 1)]))
    europe = sum(sum(emi_matrix[europe_down:(europe_up + 1), europe_left:(europe_right + 1)]))
    asia = sum(sum(emi_matrix[asia_down:(asia_up + 1), asia_left:(asia_right + 1)]))
    oceania = sum(sum(emi_matrix[oceania_down:(oceania_up + 1), oceania_left:(oceania_right + 1)]))
    china = sum(sum(emi_matrix[china_down:(china_up + 1), china_left:(china_right + 1)]))
    return americas, africa, europe, asia, oceania, china


