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

data_electric_heating = """
year	c1	P1	c2	P2	k1	k2
2015	25	3	50	160	20.64305044	-0.825691825
2020	24	3	49	160	19.70475935	-0.82050662
2030	23	3	46	160	18.9916064	-0.825691825
2050	21	3	42	160	17.34016237	-0.825691825

"""
data_solar_thermal = """
year	c1	P1	c2	P2	k1	k2	building_typ	financ_typ
2015	4000	4.2	86000	140	1139.593029	-0.125052822	existing	invest
2020	3600	4.2	81000	140	1006.727409	-0.112087865	existing	invest
2030	3400	4.2	74000	140	963.8152103	-0.121563153	existing	invest
2050	2700	4.2	67000	140	725.3841258	-0.084161465	existing	invest
2015	69	4.2	389	140	33.99818248	-0.506789025	existing	o&m fixed
2020	68	4.2	388	140	33.34097202	-0.503359795	existing	o&m fixed
2030	69	4.2	438	140	32.38686549	-0.4729554	existing	o&m fixed
2050	63	4.2	404	140	29.44782201	-0.470055762	existing	o&m fixed
2015	2700	4.2	81000	140	671.1831766	-0.030046706	new	invest
2020	2400	4.2	74000	140	589.9547408	-0.022233068	new	invest
2030	2100	4.2	67000	140	509.0440947	-0.01249163	new	invest
2050	1900	4.2	60000	140	462.5025389	-0.015418887	new	invest
2015	69	4.2	389	140	33.99818248	-0.506789025	new	o&m fixed
2020	68	4.2	388	140	33.34097202	-0.503359795	new	o&m fixed
2030	69	4.2	438	140	32.38686549	-0.4729554	new	o&m fixed
2050	63	4.2	404	140	29.44782201	-0.470055762	new	o&m fixed

"""
from io import StringIO
import pandas as pd 
data_electric_heating = pd.read_csv(StringIO(data_electric_heating),sep="\t",index_col=0)
data_solar_thermal = pd.read_csv(StringIO(data_solar_thermal),sep="\t",index_col=0)


