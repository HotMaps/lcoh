import os
import sys
import pandas as pd
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)


def projection_new(inDict, building_class):
    temp1 = str(inDict)
    temp1 = temp1.replace("\'","\"")
    df1 = pd.read_json(temp1, orient='index')
    # create indicator lists for the lowest LCOH in different building classes
    indictor_list = []
    global_min = 1e10
    best_tech = ""
    for key1 in inDict.keys():
        if inDict[key1]['Levelized costs of heat'] < global_min:
            global_min = inDict[key1]['Levelized costs of heat']
            best_tech = key1
    indictor_list.append({"unit": "EUR/kWh", "name": "Lowest LCOH for the given parameters within the building class \"" + building_class.upper() + "\" belongs to " + best_tech.upper(), "value": global_min})
    
    for key1 in inDict.keys():
        if key1 == best_tech:
            continue
        lcoh = inDict[key1]['Levelized costs of heat']
        # indictor_list.append({"unit": "EUR/kWh", "name": "Levelized cost of heat for the given parameters within the building class \"" + building_class.upper() + "\" for the technology: " + best_tech.upper(), "value": lcoh})
        indictor_list.append({"unit": "EUR/kWh", "name": "LCOH in building class \"" + building_class.upper() + "\" for the technology: " + best_tech.upper(), "value": lcoh})

    # create bar charts
    technologies = df1.index.tolist()
    economic_parameters = list(df1.columns)
    yLabel_dict = {
            'Capital Expenditure (CAPEX)': "CAPEX (EUR)",
            'Energy costs': "Energy Costs (EUR)",
            'Final energy demand': "Final Energy Demand (kWh)",
            'Levelized costs of heat': "LCOH (EUR/kWh)",
            'Operational Expenditure (OPEX)': "OPEX (EUR)",
            'Total costs': "Total Costs (EUR)"
            }
    num_of_bars = len(technologies)
    graphics = [] 
    for parameter in economic_parameters:
        temp = {"type": "bar",
                "xLabel": "Technologies",
                "yLabel": yLabel_dict[parameter],
                "data": {"labels": df1.index.tolist(),
                         "datasets": [{"label": yLabel_dict[parameter],
                                       "backgroundColor": ["#3e95cd"]*num_of_bars,
                                       "data": list(df1[parameter].values)}]
                                       }}
        graphics.append(temp)
    return graphics, indictor_list
