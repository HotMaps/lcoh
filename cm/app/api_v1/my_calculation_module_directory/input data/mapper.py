# -*- coding: utf-8 -*-
"""
Created on Wed May 15 19:27:19 2019

@author: hasani

This Module maps the differtent names in the input data to common 
names in order to do the calculation automatically
"""
# =============================================================================
# SETNav energy carrier mapping to avialable technologies in Hotmaps Heating 
# Technologies dataset
# =============================================================================
fuel_type_map = {'HP Air-to-Air': 'Electricity',
             'HP Air-to-Water': 'Electricity',
             'HP Brine-to-Water': 'Electricity',
             'Electric heater': 'Electricity',
             'Bio-oil boiler': 'Light fuel oil',
             'Oil boiler': 'Light fuel oil',
             'Biomass_Automatic': 'Biomass solid',
             'Biomass_Manual': 'Biomass solid',
             'Wood stove': 'Biomass solid',
             'Natural gas': 'Natural Gas',
             'Solar thermal': 'solar'}
# =============================================================================
# Map differnt convenentin of country shortcuts from SetNav to NUTS Convention
# =============================================================================
setNav_string = """
AUT
BEL
BGR
HRV
CYP
CZE
DNK
EST
FIN
FRA
DEU
GRC
HUN
IRL
ITA
LVA
LTU
LUX
MLT
NLD
POL
PRT
ROU
SVK
SVN
ESP
SWE
GBR
"""
setNav_code= [x.strip() for x in setNav_string.split("\n")]

nuts_string = """
AT
BE
BG
HR
CY
CZ
DK
EE
FI
FR
DE
EL
HU
IE
IT
LV
LT
LU
MT
NL
PL
PT
RO
SK
SI
ES
SE
UK
"""
nuts_code= [x.strip() for x in nuts_string.split("\n")]

setNav_code_map = dict(zip(nuts_code,setNav_code))
setNav_code_map.pop("")

# =============================================================================
# 
# =============================================================================
"""
c1&c2: Fixed O&M (€/unit/year)
P1&P2: Heat production capacity for one unit (kW)

1...One-famely house, new building	
2...Apartment complex, new building	

c = k1 * P ** k2
 
"""

data = """
year	c1	P1	c2	P2	k1	k2
2015	25	3	50	160	20.64305044	-0.825691825
2020	24	3	49	160	19.70475935	-0.82050662
2030	23	3	46	160	18.9916064	-0.825691825
2050	21	3	42	160	17.34016237	-0.825691825

"""
from io import StringIO
import pandas as pd 
data_electric_heating = pd.read_csv(StringIO(data),sep="\t",index_col=0)



