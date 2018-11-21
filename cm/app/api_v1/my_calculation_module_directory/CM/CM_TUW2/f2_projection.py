import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)


def data_matrix(inDict, building_class, techs, data_components,
                colors=('r', 'y', 'b')):
    N_bc = len(building_class)
    N_tech = len(techs)
    N_comp = len(data_components)
    data = np.zeros((N_bc, N_tech, N_comp))
    ind = np.delete(np.arange(3*N_tech + 2), [N_tech, 2*N_tech])
    _width = 0.35
    fig, ax = plt.subplots()
    for i, item0 in enumerate(building_class):
        for j, item1 in enumerate(techs):
            for k, item2 in enumerate(data_components):
                data[i, j, k] = inDict[item0][item1][item2]
    bottom = np.zeros(N_bc * N_tech)
    for i in range(N_comp):
        temp = data[:, :, i].flatten()
        ax.bar(ind, temp, _width, bottom=bottom, align='center', color=colors[i])
        bottom += temp
    plt.xticks(rotation=45)
    ax.set_xticks(ind)
    ax.set_xticklabels(techs*N_bc)
    ax.legend(data_components*N_bc, loc='upper right')
    plt.show()
    fig = ax = None


def projection(inDict):
    building_class = list(inDict.keys())
    techs = list(inDict[building_class[0]].keys())
    components = ['Capital Expenditure (CAPEX)',
                  'Operational Expenditure (OPEX)',
                  'Energy costs',
                  'Levelized costs of heat',
                  'Final energy demand']
    data_matrix(inDict, building_class, techs, components[:3], ('r', 'y', 'b'))
    data_matrix(inDict, building_class, techs, components[3:4], ('g'))
    data_matrix(inDict, building_class, techs, components[4:], ('b'))

