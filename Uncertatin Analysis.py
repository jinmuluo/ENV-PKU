import numpy as np
import math
import random
import matplotlib.pyplot as plt


def monte_carlo(emi_factor=0.1, burn_area=0.1, fuel_load=0.1, com_efficient=0.1):
    # ----------------------------------------------------------------------------------------------------------------------
    # Define the variables.
    # ----------------------------------------------------------------------------------------------------------------------
    EF = 0.35
    BA = 0.10
    FL = 0.10
    CE = 0.50
    EMI = 0
    times = 200000
    # ----------------------------------------------------------------------------------------------------------------------
    # Monte Carlo simulation and return the results.
    # ----------------------------------------------------------------------------------------------------------------------
    result = []
    for i in range(times):
        ef_term = np.random.uniform(low=emi_factor - emi_factor*EF, high=emi_factor + emi_factor*EF)
        ce_term = np.random.uniform(low=com_efficient-com_efficient*CE, high=com_efficient + com_efficient*CE)
        ba_term = np.random.normal(loc=burn_area, scale=burn_area*BA)
        fl_term = np.random.normal(loc=fuel_load, scale=fuel_load*FL)
        # result.append(math.log(ef_term*ba_term*fl_term*ce_term,10))
        result.append(ef_term*ba_term*fl_term*ce_term)
        print('Process', round(i/times * 100), '% --')
    mean_value = np.mean(result)
    std = np.std(result)
    print(mean_value, std, std/mean_value)
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.hist(result, bins=50, color='green', alpha=0.7)
    ax.set_xlabel('BaP(tons)', size=25)
    ax.set_ylabel('Frequency', size=25)
    ax.tick_params(labelsize=25)
    # ax.set_xlim(min(result)-20, max(result)+20)
    # ax.set_ylim(0, 2000)
    ax.grid()
    plt.show()


print(monte_carlo(emi_factor=0.1, burn_area=60, fuel_load=20, com_efficient=0.2))
