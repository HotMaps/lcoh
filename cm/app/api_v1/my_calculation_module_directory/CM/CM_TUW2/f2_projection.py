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
    

    
    graphics  = [
            {
                    "type": "bar",
                    "xLabel": "",
                    "yLabel": "Potential(GWh/year)",
                    "data": {
                            "labels": [str(x) for x in range(len(DHPot))],
                            "datasets": [{
                                    "label": "Calculation module chart",
                                    "backgroundColor": ["#3e95cd"]*len(DHPot),
                                    "data": list(DHPot)
                                    }]
                    }
                }]
    
    
    




def projection_new(inDict):
    keys = list(inDict.keys())
    temp1 = str(inDict[keys[0]])
    print('temp1: ', temp1)
    temp1 = temp1.replace("\'","\"")
    temp2 = str(inDict[keys[1]])
    temp2 = temp2.replace("\'","\"")
    temp3 = str(inDict[keys[2]])
    temp3 = temp3.replace("\'","\"")
    df1 = pd.read_json(temp1, orient='index')
    df2 = pd.read_json(temp2, orient='index')
    df3 = pd.read_json(temp3, orient='index')
    
    technologies = df1.index.tolist()
    values_for_test = np.concatenate((df1['Capital Expenditure (CAPEX)'].values, df2['Capital Expenditure (CAPEX)'].values, df3['Capital Expenditure (CAPEX)'].values))
    long_label_for_test = []
    for key in keys:
        for tech in technologies:
            long_label_for_test.append(key + "_" + tech)
    
    graphics  = [
            {
                    "type": "bar",
                    "xLabel": "Technologies",
                    "yLabel": 'CAPEX (EUR)',
                    "data": {
                            "labels": df1.index.tolist(),
                            "datasets": [{
                                    "label": "CAPEX for " + keys[0],
                                    "backgroundColor": ["#3e95cd"]*len(df1.index.tolist()),
                                    "data": list(df1['Capital Expenditure (CAPEX)'].values)
                                    }]
                    }
                },
            {
                    "type": "bar",
                    "xLabel": "Technologies",
                    "yLabel": 'CAPEX (EUR)',
                    "data": {
                            "labels": long_label_for_test,
                            "datasets": [{
                                    "label": "CAPEX for all building types",
                                    "backgroundColor": ["#3e95cd"]*len(df1.index.tolist()),
                                    "data": list(values_for_test)
                                    }]
                    }
                }]
    print(graphics)
    return graphics
    






def projection_old(inDict):
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

