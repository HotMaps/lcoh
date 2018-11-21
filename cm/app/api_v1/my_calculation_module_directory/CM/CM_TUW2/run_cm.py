import os
import sys
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
import CM.CM_TUW2.f1 as F1


def main(sector, building_type, demand_type, year, gfa, r, in_df_tech_info,
         in_df_energy_price, in_df_specific_demand, in_raster_nuts_id_number):
    values = F1.main(sector, building_type, demand_type, year, gfa, r,
                     in_df_tech_info, in_df_energy_price,
                     in_df_specific_demand, in_raster_nuts_id_number)
    return values
