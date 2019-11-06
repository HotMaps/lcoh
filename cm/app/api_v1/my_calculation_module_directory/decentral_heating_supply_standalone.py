# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:11:38 2019

@author: hasani
"""

# =============================================================================
# import needed modules 
# =============================================================================
import pandas as pd
import os,sys,math
from pathlib import Path
# =============================================================================
# Input Path
# =============================================================================
root_path  = os.path.dirname(os.path.realpath(__file__))
input_data_path = os.path.join(root_path,"input data")
path_building_stock = os.path.join(input_data_path,"Hotmaps","data_building_stock.csv") #TODO: Load directly from github
path_financ_heating_tec = os.path.join(input_data_path,"Hotmaps","data_Heating_technologies_EU28_v3.csv") #TODO: Load directly from github
path_setNav_retail_energy_prices = os.path.join(input_data_path,"SetNav","RetailPricesToInvert_11072018_2.xlsx")
path_dea_catalog = os.path.join(input_data_path,"DEA","technologydatafor_heating_installations_marts_2018.xlsx")
path_invert_pmin = os.path.join(input_data_path,"Invert","invert_p_min.csv")
path_load_profiles = Path(os.path.join(input_data_path,"Hotmaps","LOAD PROFILES")) #TODO: Load directly from github
# =============================================================================
# Loading and preprocessing input data
# =============================================================================

#TODO: Load directly from api
building_stock = pd.read_csv(path_building_stock,sep="|",skiprows=[0])
building_stock = building_stock[building_stock.feature == "Useful energy demand"]
grp_bdstock = building_stock.groupby(["country_code","sector","type"])

#TODO: Load directly from api
financ_heating_tec = pd.read_csv(path_financ_heating_tec,sep=";")
grp_financ_heating_tec = financ_heating_tec.groupby(["NUTS0_ID", "type_of_building","year"])


setNav_retail_energy_prices = pd.read_excel(path_setNav_retail_energy_prices)
grp_energy_prices = setNav_retail_energy_prices.groupby(["cty_abr","Sector","Tax"])  # EUR/GJ


data_pmin = pd.read_csv(path_invert_pmin)

# =============================================================================
# Decorators
# =============================================================================
import functools    
def catch_assertion_errors(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        args_repr = [repr(a) for a in args] 
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  
        signature = ", ".join(args_repr + kwargs_repr)
        try:
            value = func(*args, **kwargs)
            return value
        except AssertionError as error:
            return str(error),signature,False
    return wrapper_decorator
# =============================================================================
# Functions
# =============================================================================
# =============================================================================
def xor(a,b,tec,topic,nuts0):
    """ This function return the first not NaN value from a tuple
    
    
    Parameters
    ----------
    a: float
        hotmaps data
        
    b: float
        invert data
        
    tec: str
        Name of the heating system (only for debugging)
        
    nuts0: str
        Name of the country (only for debugging)
        
    Returns
    -------
    a|b: float
        First non NaN vale of a or b
        
    
    """
    if math.isnan(a) and not math.isnan(b):
        return 0,b
    elif math.isnan(b) and not math.isnan(a):
        return a,0
    elif math.isnan(a) and math.isnan(b):
        assert False, f"Error No available Data for <{topic}> in <{tec}> in country <{nuts0}>"
    else:
        return a,b
        
# =============================================================================
def get_pmin(nuts0,tec,data_db=data_pmin):
    assert nuts0 in set(data_db.nuts0), f"Now pmin data for <{tec}> in country <{nuts0}>"
    assert tec in set(data_db.tec), f"Now pmin data for <{tec}> in country <{nuts0}>"
    return  float(data_db.loc[(data_db.nuts0 == nuts0) & (data_db.tec == tec),"p_min"])
# =============================================================================

def get_value(nuts0,sector,hd_typ,building_stock=building_stock,
              grp_bdstock=grp_bdstock,bage=None,btype="Total"):
    """This function returns the anual usefull energy demand for either 
    Spaceheating, Hot water or Cooling Demand in kWh/m²
    
    The database behind it can be found in https://gitlab.com/hotmaps/building-stock/blob/master/data/building_stock.csv
    This function calculates the mean value from all construction period 
    of the values defined in 'hd_typ' and the sector defined in 'sector' or 
    the value specifed by the building type and building age
    
    Parameters
    ----------
    nuts0: string
        {'at', 'be', 'bg', 'cy', 'cz', 'de', 'dk', 'ee', 'es', 'eu28', 'fi', 
        'fr', 'gr', 'hr', 'hu', 'ie', 'it', 'lt', 'lu', 'lv', 'mt', 'nl', 'pl', 
        'pt', 'ro', 'se', 'si', 'sk', 'uk'}
    
    sector: string 
        {'Residential sector', 'Service sector'}
        
    
    hd_typ: string
        {"Space heating [kWh/m² year]","Domestic hot water  [kWh/m² year]",
        "Space cooling [kWh/m² year"}
                
    
    building_stock: pandas.DataFrame (6612, 14)
        This is the default Data as padnas DataFrame read from link above 
    
    grp_bdstock: pandas.core.groupby.generic.DataFrameGroupBy
        This iterator contains the DataFrames that are sorted by 
        ["country_code","sector","type"]
    
    Returns
    -------
    ued: float
        Useful energy demand of 'hd_typ' for 'sector' (mean value of all construction periods)
    
    """
    assert nuts0.lower() in set(building_stock.country_code), \
    f"The Region:<{nuts0}> is not available in the building stock dataset"
    
    assert sector in set(building_stock.sector), \
    f"The Sector:<{sector}> is not available in the building stock dataset"
    
    assert btype in set(building_stock.btype),\
    f"The building type:<{btype}> is not available in the building stock dataset"
    
    if type(bage) != type(None):
        assert bage in set(building_stock.bage),\
        f"The building age:<{bage}> is not available in the building stock dataset"

    
    df = grp_bdstock.get_group((nuts0.lower(),sector,hd_typ))
    if type(bage) == type(None):
        value = df[df.subsector == btype].value.mean() 
    else:
        value = df[ (df.bage == bage) & (df.subsector == btype) ].value.mean() # mean only to get a float type scalar
    return value
# =============================================================================
def get_ued(nuts0,sector,hd_typ,gfa,bage=None,btype="Total"):
    """ This function return the anual useful energy demand in kWH
    
    Based on the list 'hd_type' the specific usful energy demands(ued) are accumulated
    and then multiplied by the 'gfa' to get the ued in kWh
    
    Parameters
    ----------
    nuts0: string
        {'at', 'be', 'bg', 'cy', 'cz', 'de', 'dk', 'ee', 'es', 'eu28', 'fi', 
        'fr', 'gr', 'hr', 'hu', 'ie', 'it', 'lt', 'lu', 'lv', 'mt', 'nl', 'pl', 
        'pt', 'ro', 'se', 'si', 'sk', 'uk'}
    
    sector: string 
        {'Residential sector', 'Service sector'}
        
    hd_type: list  
        a list that can contain the following entries
        {"Space heating [kWh/m² year]","Domestic hot water  [kWh/m² year]",
        "Space cooling [kWh/m² year"}
        
    gfa: float
        Gross floor are in m²
        

    Returns
    -------
    ued: float
        the anual useful energy demand in kWh
    
    """
    sector = f"{sector} sector"

    # Accumulate Useful Energy Demand in kWh/(m²a)
    ued = sum([get_value(nuts0,sector,hd_type,bage=bage,btype=btype) for hd_type in hd_typ]) if type(hd_typ) == list else get_value(nuts0,sector,hd_typ,bage=bage,btype=btype)
    
    # Useful Energy Demand in kWh/a
    ued = gfa * ued
    
    
    return ued
# =============================================================================
def get_profile(nuts_code,sector,typ,input_path=path_load_profiles):
    return pd.read_csv(input_path.joinpath(sector,typ,f"{nuts_code}.csv")).load.values

def get_peaks(nuts_code,sector,input_path=path_load_profiles):
    sh = get_profile(nuts_code,sector,"space_heating",input_path=input_path)
    hw = get_profile(nuts_code,sector,"hot_water",input_path=input_path)
    arg_max_sh = sh.argmax()
    f_sh = sh[arg_max_sh] 
    f_hw = hw[arg_max_sh]
    return f_sh,f_hw
# =============================================================================  
def lcoh(energy_demand, heat_load, energy_price,
                            specific_investment_cost, fix_o_and_m, var_o_and_m,
                            efficiency_heatingsystem, r, lt):
    """ This function calculates the Levelized Costs of Heating for a heating 
    system that has constant variable costs and heat production over its life time 
    

    Parameters
    ----------
    energy_demand: float-like
        in kWh
        
    heat_load: float-like
        in kW
    
    energy_price: float-like
        EUR/kWh
    
    specific_investment_cost: float-like
        inEUR/kW
    
    fix_o_and_m: float-like
        in EUR/kW       
    
    var_o_and_m: float-like
        in EUR/kWh
    
    efficiency_heatingsystem: float-like
    
    r: float-like
        -
    
    lt: float-like
        in year

        

    Returns
    -------
    output: dict
    
    """
    q = 1 + r
    assert q != 0 or q != 1 ,"Error in calculation annuity factor ! Please choose an other interest rate."
    annuity_factor = (1-q**lt)/(q**lt*(1-q))

    # final energy demand (kWh)
    if efficiency_heatingsystem == 0:
        fed = efficiency_heatingsystem
    else:
        fed = energy_demand / efficiency_heatingsystem  

    # OPEX: Operational Expenditure (EUR)
    OPEX = fix_o_and_m * heat_load + var_o_and_m * fed

    # CAPEX: Capital Expenditure (EUR)
    CAPEX = heat_load * specific_investment_cost 
    # energy costs (EUR)
    energy_costs = fed * energy_price
    # total costs heat supply (EUR)
    OPEX_ = annuity_factor * (OPEX + energy_costs)
    
    present_value = OPEX_ + CAPEX
    
    # LCOH [EUR/kWh]
    energy_demand_ = (energy_demand * annuity_factor)
    if energy_demand == 0:
        lcoh = 0
    else:
        lcoh = present_value / energy_demand_

    output = {'Final energy demand': float(fed),
              'Capital Expenditure (CAPEX)': float(CAPEX),
              'Operational Expenditure (OPEX)': float(OPEX),
              "OPEX * annuity_factor": float(OPEX_),
              'Energy costs': float(energy_costs),
              'Total costs': float(present_value),
              "energy_demand * annuity_factor":float(energy_demand_),
              "energy_demand":float(energy_demand),
              'Levelized costs of heat': float(lcoh),
              "capex":CAPEX/energy_demand_,
              "opex":OPEX_/energy_demand_,
              "specific_investment_cost":specific_investment_cost,
              "heat_load":heat_load,
              "fed":fed,
              "opex_fix_":annuity_factor*fix_o_and_m * heat_load/energy_demand_,
              "opex_var_":annuity_factor*var_o_and_m * fed/energy_demand_,
              "opex_":annuity_factor*OPEX/energy_demand_,
              "energy_costs_":annuity_factor *energy_costs/energy_demand_,
              "anuity_factor":annuity_factor,
              "energy_demand_":energy_demand_,
              "efficiency_heatingsystem":efficiency_heatingsystem,
              "energy_price":energy_price}
    return output
# =============================================================================
if input_data_path not in sys.path:
    sys.path.append(input_data_path)
from mapper import setNav_code_map,fuel_type_map,data_electric_heating
def get_energy_price(nuts0,tec,year,sector='Residential',
                     tax='Including tax but no VAT',
                     setNav_code_map=setNav_code_map,
                     grp_energy_prices=grp_energy_prices,
                     setNav_retail_energy_prices=setNav_retail_energy_prices):
    """This function returns the retail energy prices in EUR/kWh for a specific 
    NUTS0 region, year and Technology
    
    The data behind come from the SetNav Project

    Parameters
    ----------
    
    Returns
    -------
    
    """
    assert nuts0 in setNav_code_map.keys(), \
    f"The Region <{nuts0} is not in the retail price dataset"
    assert sector in set(setNav_retail_energy_prices.Sector), \
    f"The sector <{sector}> is not in the retail energy price dataset"
    assert tax in set(setNav_retail_energy_prices.Tax), \
    f"There is no value <{tax}> in the tax column in the retail energy price dataset"
    assert f"Y{year}" in set(setNav_retail_energy_prices.columns),\
    f"No data for the year {year} in the retail energy price dataset"
    assert tec in fuel_type_map.keys(), \
    f"No Energy Carriere specified for the technology: <{tec}>"
    
    df = grp_energy_prices.get_group((setNav_code_map[nuts0],sector,tax))
    df = df.set_index(df["Energy Carrier"])
    ec = fuel_type_map[tec]
    year = f"Y{year}"
    
    energy_price = 0 if ec == "solar" else df.loc[ec,year] * 0.0036 # factor for EUR/GJs -> EUR/kWh


    return energy_price
# =============================================================================
def get_tec_data(df,tec,heat_load,nuts0):
    """This function return the data for the heating system in a specifc NUTS 0
    region, year and sector

    Parameters
    ----------
    df: pandas.DataFrame 
        Prefiltered data by nuts0 region,building type and year
        
    tec: Heating System
        {"Oil boiler","HP Brine-to-Water","Wood stove","Bio-oil boiler",
        "HP Air-to-Water","Electric heater","Solar thermal","Biomass_Manual",
        "HP Air-to-Air","Biomass_Automatic","Natural gas"}
    
    Returns
    -------
    
    
    """
    financ_data_columns = ['variable_O_and_M', 'technical_lifetime', 
                   'total_annual_net_efficiency', 'k1_specific_investment_costs', 
                   'k2_specific_investment_costs', 'k1_fixed_O_and_M', 
                   'k2_fixed_O_and_M']
    
    var_o_and_m, lifetime, efficiency, k1_specific_investment_cost, \
    k2_specific_investment_cost, k1_fix_o_and_m, k2_fix_o_and_m = df.loc[tec,financ_data_columns]
    # specific investment cost in EUR/kW
    
    p_min_invert = get_pmin(nuts0,tec)
    
    
    if math.isnan(var_o_and_m):
#        print(f"No Variable Operational and Maintance Costs for <{tec}> in country <{nuts0}>, ...using 0 as default")
        var_o_and_m = 0
    if tec == "Solar thermal" and math.isnan(efficiency):
        efficiency = 1
    
    if tec == "Electric heater":
        index = df.loc[tec,"equipment_and_maintenance_index"]
        k1_fix_o_and_m = data_electric_heating.loc[int(df.year[tec]),"k1"]*index
        k2_fix_o_and_m = data_electric_heating.loc[int(df.year[tec]),"k2"]
        
    if heat_load < p_min_invert:
        heat_load = p_min_invert
    
    k1_specific_investment_cost, k2_specific_investment_cost = \
    xor(k1_specific_investment_cost, k2_specific_investment_cost,tec,
        "invest",nuts0)
    

    specific_investment_cost = k1_specific_investment_cost * (heat_load**k2_specific_investment_cost)
    if specific_investment_cost == float("nan"):
        assert False,f"Error: No specific investment costs for {tec}, {nuts0}"
    
    
    k1_fix_o_and_m, k2_fix_o_and_m = xor(k1_fix_o_and_m, k2_fix_o_and_m,tec,
                                         "maintainance",nuts0)
    
    fix_o_and_m = k1_fix_o_and_m * (heat_load**k2_fix_o_and_m)
    if fix_o_and_m == float("nan"):
        assert False,f"Error: No fixed operational and maintainance costs for {tec}, {nuts0}"

    return specific_investment_cost,fix_o_and_m,var_o_and_m,efficiency,lifetime,heat_load
# =============================================================================
def lcoh_per_tec(r,nuts0,building_typ,year,heating_energy_demand,heat_load,
                 grp_financ_heating_tec=grp_financ_heating_tec,
                 financ_heating_tec = financ_heating_tec):
    """This function calculates the LCOH for each technology and specific 
    building type at a specific year for a NUTS0 region
    
    Parameters
    ----------
    
    Returns
    -------
    
    """
    assert type(year) == int, f"The Year <{year}> is not an interger"
    assert year in set(financ_heating_tec.year), \
    f"The year:<{year}> is not available in the financal dataset for heating systems"
    assert building_typ in set(financ_heating_tec.type_of_building),\
    f"The bulding type:<{building_typ}> is not available in the financal dataset for heating systems"
    
    df = grp_financ_heating_tec.get_group((nuts0,building_typ,year))
    df = df.set_index(df.heating_equipment)
    df = df.drop(["DH substation"])
#    df = df.drop(["Bio-oil boiler"]) # XXX: No fuel prices for bio oil , therefore drop this heating system
    out = dict()
    for tec in df.index:
        #XXX: heat_load2
        specific_investment_cost,fix_o_and_m,var_o_and_m,efficiency,lifetime,heat_load2 = \
            get_tec_data(df,tec,heat_load,nuts0)
        
        energy_price = get_energy_price(nuts0,tec,year)
        
        out[tec] = lcoh(heating_energy_demand, heat_load2,
                       energy_price, specific_investment_cost, fix_o_and_m,
                       var_o_and_m, efficiency, r, lifetime)
    return out
# =============================================================================
# 
# =============================================================================
def get_nuts(nuts_code):
    nuts3 = nuts_code[:5]
    nuts2 = nuts_code[:4]
    nuts1 = nuts_code[:3]
    nuts0 = nuts_code[:2]
    return nuts3,nuts2,nuts1,nuts0    

@catch_assertion_errors
def main(nuts_code,sav,gfa,year,r,bage,btype,*ef_args):
    serv = ['Trade', 'Other non-residential buildings', 'Hotels and Restaurants', 'Offices', 'Health', 'Education']
    res=['Multifamily houses', 'Single family- Terraced houses', 'Appartment blocks']
    building_types = dict(zip(res+serv,['existing MFH','existing SFH','existing MFH']+['existing MFH'] * len(serv)))
    sector_mapper = {**dict(zip(serv,["Service"]*len(serv))),**dict(zip(res,["Residential"]*len(res)))}
    sector = sector_mapper[btype]
    building_type = building_types[btype]
    if sav*100 > 0:
        building_type=building_type.replace("existing","new")
    _nuts3,nuts2,nuts1,nuts0 = get_nuts(nuts_code)
    ued_sh = get_ued(nuts0,sector,"Space heating [kWh/m² year]",gfa,bage,btype) # spcae heating demand kWh
    ued_hw = get_ued(nuts0,sector,"Domestic hot water  [kWh/m² year]" ,gfa,bage,btype) # hot water demand kWh
    ued = ued_sh + ued_hw
    f_sh,f_hw = get_peaks(nuts2,f"{sector.lower()}_sector")  # pmax factor in 1/h
    heat_load_sh = ued_sh*f_sh*(1-sav)  # Pmax in kW
    heat_load_hw = ued_hw*f_hw  # Pmax in kW
    heat_load = 1.2*(heat_load_sh + heat_load_hw)   # Pmax in kW
    result = lcoh_per_tec(r,nuts0,building_type,year,ued,heat_load)
    return result,(ued,heat_load,building_type,sector),True

if __name__ == "__main__":
    print("Calculation started")
# =============================================================================
# %%  User-Input
# =============================================================================
    nuts_code = "DE71" 
    sav = 0 # savings in % [0,1]
    gfa = 150  # Gross Floor Area in m² 
    year = 2015 # int
    r = 0.01 # interest rate
    bage = "Before 1945" # None for mean value
    btype = "Single family- Terraced houses" # "Total" for mean value
# =============================================================================
#%%   "Algorithm"
# =============================================================================
    results,inputs,ok = main(nuts_code=nuts_code,sav=sav,gfa=gfa,year=year,r=r,bage=bage,btype=btype)

# =============================================================================
#     
# =============================================================================
    print("Calculation Done")
    