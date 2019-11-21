# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 18:24:29 2019

This module provide some functions for manupulating hotmaps data input for my 
needs

@author: 
"""
from ..my_calculation_module_directory.raster_api import return_nuts_codes
import os,sys
root_path  = os.path.dirname(os.path.realpath(__file__))
input_data_path = os.path.join(root_path,"input data")
if input_data_path not in sys.path:
    sys.path.append(input_data_path)
from mapper import fuel_type_map


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
            dict(unit=" % ",name="savings in space heating (%)",value=sav*100),
            dict(unit="m2",name="gross floor area (m2)",value=gfa),
            dict(unit=" ",name="year",value=year),
            dict(unit="%",name="interest rate",value=r*100),
            dict(unit="-",name=f"building age: {bage}",value=0),
            dict(unit="-",name=f"building type: {btype}",value=0)]
    if ok:
        ued,heat_load,building_type,sector = inputs2
        out_list2= [dict(unit="kWh/yr",name="useful energy demand",value=round(ued,2)),
                dict(unit="kW",name="heat load - Qmax (kW)",value=round(heat_load,0)),
                dict(unit="-",name=f"sector: {sector}",value=0),
                dict(unit="-",name=f"used building type for financial  data: {building_type}",value=0)]
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
        tec = list(results)
        solution = dict()
        solution["Levelized cost of heat (EUR/MWh)"] = [round(results[tec]["Levelized costs of heat"]*1e3,2) for tec in tec]
        solution["Energy price (EUR/MWh)"] = [round(results[tec]["energy_price"]*1e3,2) for tec in tec]
        solution["CAPEX (EUR/yr)"] = [round(results[tec]["Capital Expenditure (CAPEX)"],2) for tec in tec]
        solution["Energy Costs (EUR/yr)"] = [round(results[tec]["Energy costs"],2) for tec in tec]
        solution["Final Energy Demand (MWh/yr)"] = [round(results[tec]["Final energy demand"]*1e-3,2) for tec in tec]
        solution["OPEX (EUR/yr)"] = [round(results[tec]["Operational Expenditure (OPEX)"],2) for tec in tec]
        solution["Total Costs (EUR/yr)"] = [round(results[tec]["Total costs"],2) for tec in tec]
        solution["Anuity Factor"] = [round(results[tec]["anuity_factor"],2) for tec in tec]
        solution["Efficiency heating system (%)"] = [round(results[tec]["efficiency_heatingsystem"]*1e2,2) for tec in tec]
#        solution["Heat Load (kW)"] = [round(results[tec]["heat_load"],2) for tec in tec]
        *_,ef_elec,ef_oil,ef_biomas,ef_gas=inputs
        
        emission_factor_map = {'Electricity':ef_elec,
                               'Light fuel oil':ef_oil,
                               'Biomass solid':ef_biomas,
                               'Natural Gas':ef_gas,
                               'solar':0,}
        
        solution["CO2 Emission (tCO2/yr)"] = [round(results[tec]["fed"]*1e-3*emission_factor_map[fuel_type_map[tec]],2) for tec in tec]
        _,color = color_my_list(tec)
 
       
        list_of_tuples = [dict(type="bar",label=label) for label in solution]
        graphics = [ dict( xLabel="Technologies",
                           yLabel=x["label"],
                          type = x["type"],
                           data = dict( labels = tec,
                                        datasets = [ dict(label=x["label"],
                                                          backgroundColor = color ,
                                                          data = solution[x["label"]])] )) for x in list_of_tuples]
        
        indicators = generate_input_indicators(inputs,inputs2,True)
        
        return indicators,graphics