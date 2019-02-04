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
    # #######################################################################
    # remove solar thermal technology from the dictionary and dataframe
    if "Solar thermal" in df1.index:
        df1 = df1.drop(["Solar thermal"])
    if "Solar thermal" in inDict.keys():
        inDict.pop("Solar thermal", None)
    # create indicator lists for the lowest LCOH in different building classes
    indicator_list = []
    global_min = 1e10
    best_tech = ""
    for key1 in inDict.keys():
        if inDict[key1]['Levelized costs of heat'] < global_min:
            global_min = inDict[key1]['Levelized costs of heat']
            best_tech = key1
    indicator_list.append({"unit": "EUR/MWh", "name": "Lowest LCOH for the given parameters within the building class \"" + building_class.upper() + "\" belongs to " + best_tech.upper(), "value": global_min})
    for key1 in inDict.keys():
        if key1 == best_tech:
            continue
        lcoh = inDict[key1]['Levelized costs of heat']
        # indicator_list.append({"unit": "EUR/MWh", "name": "Levelized cost of heat for the given parameters within the building class \"" + building_class.upper() + "\" for the technology: " + best_tech.upper(), "value": lcoh})
        indicator_list.append({"unit": "EUR/MWh", "name": "LCOH in building class \"" + building_class.upper() + "\" for the technology: " + key1.upper(), "value": lcoh})

    # create bar charts
    technologies = df1.index.tolist()
    # economic_parameters = list(df1.columns)
    economic_parameters = ['Energy costs', 'Levelized costs of heat', 'Total costs']
    yLabel_dict = {
            'Capital Expenditure (CAPEX)': "CAPEX (EUR)",
            'Energy costs': "Energy Costs (EUR)",
            'Final energy demand': "Final Energy Demand (kWh)",
            'Levelized costs of heat': "LCOH (EUR/MWh)",
            'Operational Expenditure (OPEX)': "OPEX (EUR)",
            'Total costs': "Total Annual Costs (EUR)"
            }
    num_of_bars = len(technologies)
    graphics = [] 
    
    for parameter in economic_parameters:
        temp = {"type": "bar",
                "xLabel": "Technologies",
                "yLabel": yLabel_dict[parameter],
                "data": {"labels": technologies,
                         "datasets": [{"label": yLabel_dict[parameter],
                                       "backgroundColor": ["#3e95cd"]*num_of_bars,
                                       "data": list(df1[parameter].values)}]
                                       }}
        graphics.append(temp)
    return graphics, indicator_list
