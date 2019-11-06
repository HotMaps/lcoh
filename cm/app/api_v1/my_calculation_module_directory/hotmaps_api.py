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
    Category20=[ '#1f77b4',
                 '#aec7e8',
                 '#ff7f0e',
                 '#ffbb78',
                 '#2ca02c',
                 '#98df8a',
                 '#d62728',
                 '#ff9896',
                 '#9467bd',
                 '#c5b0d5',
                 '#8c564b',
                 '#c49c94',
                 '#e377c2',
                 '#f7b6d2',
                 '#7f7f7f',
                 '#c7c7c7',
                 '#bcbd22',
                 '#dbdb8d',
                 '#17becf',
                 '#9edae5']               
    l = len(liste)
    if 8<l<21:
        return dict(zip(liste,Category20)),Category20
    elif 2<l<9:
        colors = color_blind_palette[l]
        return dict(zip(liste,colors)),colors
    else:
        colors = ["#b3e2cd"]*l
        return dict(zip(liste,colors)),colors
        
def generate_input_indicators(inputs,inputs2,ok):
    nuts_code,sav,gfa,year,r,bage,btype,ef_elec,ef_oil,ef_biomas,ef_gas = inputs
    
    out_list1 = [dict(unit="-",name=f"NUTS code: {nuts_code}",value=0),
            dict(unit="%",name="savings in space heating",value=sav*100),
            dict(unit="m2",name="gross floor area",value=gfa),
            dict(unit=" ",name="year",value=year),
            dict(unit="%",name="interest rate",value=r*100),
            dict(unit="-",name=f"building age: {bage}",value=0),
            dict(unit="-",name=f"building type: {btype}",value=0)]
    if ok:
        ued,heat_load,building_type,sector = inputs2
        out_list2= [dict(unit="kWh",name="useful energy demand",value=round(ued,2)),
                dict(unit="kW",name="Qmax",value=round(heat_load,2)),
                dict(unit="-",name=f"Sector: {sector}",value=0),
                dict(unit="-",name=f"Used Building type for finacal data: {building_type}",value=0)]
    else:
        out_list2 = [dict(unit="-",name=f"Errors: {inputs2}",value=0)]
        
    return out_list1 + out_list2

        
def get_inputs( inputs_raster_selection, inputs_parameter_selection):
    path_nuts_id_tif = inputs_raster_selection["nuts_id_number"]
    (nuts0, nuts1, nuts2, nuts3)  = return_nuts_codes(path_nuts_id_tif) 
    
    nuts_code = nuts3
    sav = float(inputs_parameter_selection["sav"]) # savings in % [0,1]
    if  not (-0.1<sav*100<100):
        return None,False,"Error Space heating savings is not int the interval [0,1]"
    gfa = float(inputs_parameter_selection["gfa"])  # Gross Floor Area in m² 

    year = int(inputs_parameter_selection["year"])
    r = float(inputs_parameter_selection["r"]) # interest rate
    if  not (0<r<1):
        return None,False, "Error interest rate is not in the interval (0,1)"
    
    bage = inputs_parameter_selection["bage"]
    btype = inputs_parameter_selection["btype"]
    
    ef_elec = float(inputs_parameter_selection["ef_elec"]) 
    ef_oil = float(inputs_parameter_selection["ef_oil"] )
    ef_biomas = float(inputs_parameter_selection["ef_biomas"])
    ef_gas = float(inputs_parameter_selection["ef_gas"])
    return (nuts_code,sav,gfa,year,r,bage,btype,ef_elec,ef_oil,ef_biomas,ef_gas),True,None

def generate_output(results,inputs,inputs2):
        solution = {"Technologies":list(results)}
        solution["Levelized cost of heat (EUR/MWh)"] = [round(results[tec]["Levelized costs of heat"]*1e3,2) for tec in solution["Technologies"]]
        solution["Energy price (EUR/MWh)"] = [round(results[tec]["energy_price"]*1e3,2) for tec in solution["Technologies"]]

        _,color = color_my_list(solution["Technologies"])
        
        list_of_tuples = [
                    dict(type="bar",label="Levelized cost of heat (EUR/MWh)"),
                    dict(type="bar",label="Energy price (EUR/MWh)"),
                    ]
        graphics = [ dict( xLabel="Technologies",
                           yLabel=x["label"],
                          type = x["type"],
                           data = dict( labels = solution["Technologies"],
                                        datasets = [ dict(label=x["label"],
                                                          backgroundColor = color ,
                                                          data = solution[x["label"]])] )) for x in list_of_tuples]
        
        indicators = generate_input_indicators(inputs,inputs2,True)
        
        return indicators,graphics