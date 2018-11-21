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


if __name__ == "__main__":
    sector = 'residential'
    building_type = 'new SFH'
    demand_type = 'heating'
    year = 2015
    gfa = 100
    r = 0.05
    import pandas as pd
    in_df_tech_info = pd.read_csv(r'C:\Users\Mostafa\Desktop\test\tech_info.csv')
    in_df_energy_price = pd.read_csv(r'C:\Users\Mostafa\Desktop\test\energy_price.csv')
    in_df_specific_demand = pd.read_csv(r'C:\Users\Mostafa\Desktop\test\specific_demand.csv')
    in_raster_nuts_id_number = r'C:\Users\Mostafa\Desktop\test\AT130_feature.tif'
    main(sector, building_type, demand_type, year, gfa, r, in_df_tech_info,
         in_df_energy_price, in_df_specific_demand, in_raster_nuts_id_number)
    
