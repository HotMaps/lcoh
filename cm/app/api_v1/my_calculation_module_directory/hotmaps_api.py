# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 18:24:29 2019

This module provide some functions for manupulating hotmaps data input for my 
needs

@author: 
"""
from ..my_calculation_module_directory.raster_api import return_nuts_codes

def color_my_list(liste):
    color_blind_palette= {   3: ['#0072B2', '#E69F00', '#F0E442'],
        4: ['#0072B2', '#E69F00', '#F0E442', '#009E73'],
        5: ['#0072B2', '#E69F00', '#F0E442', '#009E73', '#56B4E9'],
        6: ['#0072B2', '#E69F00', '#F0E442', '#009E73', '#56B4E9', '#D55E00'],
        7: [   '#0072B2',
               '#E69F00',
               '#F0E442',
               '#009E73',
               '#56B4E9',
               '#D55E00',
               '#CC79A7'],
        8: [   '#0072B2',
               '#E69F00',
               '#F0E442',
               '#009E73',
               '#56B4E9',
               '#D55E00',
               '#CC79A7',
               '#000000']}
    l = len(liste)
    if 2<l<9:
        colors = color_blind_palette[l]
        return dict(zip(liste,colors)),colors
		
def generate_input_indicators(inputs,inputs2):
    nuts_code,sav,gfa,year,r,bage,btype = inputs
    ued,heat_load,building_type,sector = inputs2
    
    return [dict(unit="none",name="nuts_code",value=f"{nuts_code}"),
            dict(unit="%",name="savings in space heating",value=f"{sav*100}"),
            dict(unit="m2",name="gross floor area",value=f"{gfa}"),
            dict(unit="none",name="year",value=f"{year}"),
            dict(unit="%",name="interest rate",value=f"{r*100}"),
            dict(unit="none",name="building age",value=f"{bage}"),
            dict(unit="none",name="btype",value=f"{btype}"),
            dict(unit="kWh",name="useful energy demand",value=f"{round(ued,2)}"),
            dict(unit="kW",name="Qmax",value=f"{round(heat_load,2)}"),
            dict(unit="none",name="Sector",value=f"{sector}"),
            dict(unit="none",name="Used Building type for finacal data",value=f"{building_type}")]
        
def get_inputs( inputs_raster_selection, inputs_parameter_selection):
    path_nuts_id_tif = inputs_raster_selection["nuts_id_number"]
    (nuts0, nuts1, nuts2, nuts3)  = return_nuts_codes(path_nuts_id_tif) 
    
    nuts_code = nuts3
    sav = float(inputs_parameter_selection["sav"]) # savings in % [0,1]
    if  not (-0.001<sav<1.001):
        return None,False,"Error Space heating savings is not int the interval [0,1]"
    gfa = float(inputs_parameter_selection["gfa"])  # Gross Floor Area in m² 

    year = int(inputs_parameter_selection["year"])
    r = float(inputs_parameter_selection["r"]) # interest rate
    if  not (0<r<1):
        return None,False, "Error interest rate is not in the interval (0,1)"
    
    bage = inputs_parameter_selection["bage"]
    btype = inputs_parameter_selection["btype"]
    
    return (nuts_code,sav,gfa,year,r,bage,btype),True,None

def generate_output(results,inputs,inputs2):
        solution = {"Technologies":list(results)}
        solution["Levelized Costs Of Heat [EUR/kWh]"] = [results[tec]["Levelized costs of heat"] for tec in solution["Technologies"]]
        solution["Energy Price [EUR/kWh]"] = [results[tec]["energy_price"] for tec in solution["Technologies"]]
        _,color = color_my_list(solution["Technologies"])
        
        list_of_tuples = [
                    dict(type="bar",label="Levelized Costs Of Heat [EUR/kWh]"),
                    dict(type="bar",label="Energy Price [EUR/kWh]"),
                    ]
        graphics = [ dict( type = x["type"],
                           data = dict( labels = solution["Technologies"],
                                        datasets = [ dict(label=x["label"],
                                                          backgroundColor = color ,
                                                          data = solution[x["label"]])] )) for x in list_of_tuples]
        
        indicators = generate_input_indicators(inputs,inputs2)
        
        return indicators,graphics