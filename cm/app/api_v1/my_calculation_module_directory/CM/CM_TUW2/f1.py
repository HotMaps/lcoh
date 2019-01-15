import os
import sys
import numpy as np
import pandas as pd
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)
from CM.CM_TUW2.LCOH import levelized_costs_of_heat as lcoh
from CM.CM_TUW2.f2_projection import projection_new as prj
from CM.CM_TUW1.read_raster import raster_array


def return_nuts_codes(in_raster):
    code_csv = path +'/CSVs/nuts_id_number.csv'
    code_list = pd.read_csv(code_csv)
    arr = raster_array(in_raster).astype(int)
    unique_val, counts = np.unique(arr, return_counts=True)
    ind_0 = np.argwhere(unique_val == 0)[0][0]
    unique_val = np.delete(unique_val, ind_0)
    # In case of region selection from several NUTS 3 areas, only the one with
    # highest number of elements is selected.
    counts = np.delete(counts, ind_0)
    ind = np.argwhere(counts == np.max(counts))[0][0]
    code = unique_val[ind]
    # Columns 3, 4, 5, 6 show nuts0, nuts1, nuts2, nuts3, respectively!
    # This csv will not change and is part of the uploaded scripts.
    [nuts0_row, nuts1_row, nuts2_row, nuts3_row] = code_list[code_list['id'] == code].values[:, [3, 4, 5, 6]][0]
    code_list_values = code_list.values
    nuts0 = code_list_values[nuts0_row, 1]
    nuts1 = code_list_values[nuts1_row, 1]
    nuts2 = code_list_values[nuts2_row, 1]
    nuts3 = code_list_values[nuts3_row, 1]
    return nuts0, nuts1, nuts2, nuts3   


def return_columns(df):
    column_names = df.columns
    indices = []
    indices.append(np.argwhere(column_names == 'heating_equipment')[0][0])
    indices.append(np.argwhere(column_names == 'variable_o_and_m')[0][0])
    indices.append(np.argwhere(column_names == 'technical_lifetime')[0][0])
    indices.append(np.argwhere(column_names == 'total_annual_net_efficiency')[0][0])
    indices.append(np.argwhere(column_names == 'k1_specific_investment_costs')[0][0])
    indices.append(np.argwhere(column_names == 'k2_specific_investment_costs')[0][0])
    indices.append(np.argwhere(column_names == 'k1_fixed_o_and_m')[0][0])
    indices.append(np.argwhere(column_names == 'k2_fixed_o_and_m')[0][0])
    return indices


def load_factor(nuts2_code, sector, hoc='heating'):
    file_path = path + '/CSVs/AD.TUW2_120_percent_max_load_factor.csv'
    df = pd.read_csv(file_path)
    factor = df[(df['nuts2_id'] == nuts2_code) &
                (df['heating_or_cooling'] == hoc) &
                (df['sector'] == sector)].values[:, 3]
    df = None
    return factor[0]


def fuel_prices(df, nuts0_code, year, fuel_type_column=3,
                fuel_cost_column=4):
    # filter dataframe based on nuts code and year
    df_filtered_val = df[(df['year'] == int(year)) & (df['nuts0'] == nuts0_code)].values
    fc = dict()
    for row in range(df_filtered_val.shape[0]):
        f_type, f_cost = df_filtered_val[row, [3, 4]]
        fc[f_type] = f_cost
    print("fc ",fc)
    return fc


def main(sector, building_type, demand_type, year, gfa, r, in_df_tech_info,
         in_df_energy_price, in_df_specific_demand, in_raster_nuts_id_number):
    '''
    # check input types
    if sector not in ('residential', 'service'):
        raise ValueError('The sector should be either "residential" or "service"!')
    if building_type not in ('new SFH', 'new MFH', 'service'):
        raise ValueError('The building type has not been correctly selected!')
    if type(year) != int:
        raise TypeError('Year should be of integer type!')
    if type(GFA) != float and type(GFA) != int:
        raise TypeError('Gross floor area should be of float or integer type!')
    if type(r) != float and type(r) != int:
        raise TypeError('Interest rate should be of float or integer type!')
    '''
    fuel_type = {'HP Air-to-Air': 'electricity',
                 'HP Air-to-Water': 'electricity',
                 'HP Brine-to-Water': 'electricity',
                 'Electric heater': 'electricity',
                 'Bio-oil boiler': 'oil',
                 'Oil boiler': 'oil',
                 'Biomass_Automatic': 'biomass',
                 'Biomass_Manual': 'biomass',
                 'Wood stove': 'wood',
                 'Natural gas': 'gas',
                 'Solar thermal': 'solar'}
    building_type_assignment = {
            "Service sector (average)": "service",
            "Single family house": "new SFH",
            "Multi family house": "new MFH"
            }
    building_status_energy_factor = {'existing building': 1,
                                     'renovated building': 0.5,
                                     'new building': 0.3
                                     }
    building_type = building_type_assignment[building_type]
    nuts0, nuts1, nuts2, nuts3 = return_nuts_codes(in_raster_nuts_id_number)
    '''
    extract data from tech info sheet for the give country and year and
    considering following columns:
    3: heating_equipment
    13: variable_O_and_M
    14: technical_lifetime
    15: total_annual_net_efficiency
    16: k1_specific_investment_costs
    17: k2_specific_investment_costs
    19: k1_fixed_O_and_M
    20: k2_fixed_O_and_M
    '''
    # since no separate data for service sector is available, the values for
    # the multi family houses are considered for the service sector as well.
    required_columns = return_columns(in_df_tech_info)
    info_val = in_df_tech_info[(in_df_tech_info['year'] == int(year)) &
                            (in_df_tech_info['type_of_building'].str.replace(" ", "") == building_type.replace(" ", ""))
                            ].values[:, required_columns]
    # TODO: cells that are empty are assigned a small value to avoid division
    # by zero error
    info_val[info_val == 'None'] = '0.0001'
    info_val[:, 1:] = info_val[:, 1:].astype(float)
    in_df_tech_info = None

    # get factor for sizing the heating/cooling system
    factor = load_factor(nuts2, sector)
    # get fuel prices in selected country


    energy_prices = fuel_prices(in_df_energy_price, nuts0, year)

    # get specific h&c and hot water demand in country
    [sp_heat, sp_dhw, sp_cold] = in_df_specific_demand[
            (in_df_specific_demand['nuts0_code'] == nuts0) &
            (in_df_specific_demand['sector'] == sector)
            ].values[:, [2, 3, 4]][0]
    # TODO: data base should become complete! default values for missing data
    # in csv data set; flag for use of default values.
    default_dict = {
            'var_o_and_m': 0.025,
            'lifetime': 20,
            'efficiency': 0.9,
            'k1_specific_investment_cost': 1600,
            'k2_specific_investment_cost': -0.52,
            'k1_fix_o_and_m': 53,
            'k2_fix_o_and_m': -0.56
            }
    var_o_and_m, lifetime, efficiency, k1_specific_investment_cost, \
    k2_specific_investment_cost, k1_fix_o_and_m, k2_fix_o_and_m = np.zeros(7)
    # b_type: building type ; b_lcoh: building levelized cost of heat

    output = dict()
    building_status = dict()
    for key in building_status_energy_factor.keys():
        for i in range(info_val.shape[0]):


            technology, var_o_and_m, lifetime, efficiency, \
            k1_specific_investment_cost, k2_specific_investment_cost, \
            k1_fix_o_and_m, k2_fix_o_and_m = info_val[i, :]
            # DH is not considered as decentral heating system.
            if technology == 'DH substation':
                continue
            if 'None' in info_val[i, :]:
                print('Data base has some missing numbers. Please contact the \
                      the data provider. The outputs are not correct.')
                print('The following parameters are used instead of missing \
                      data: \n\t', default_dict)
                var_o_and_m, lifetime, efficiency, \
                k1_specific_investment_cost, k2_specific_investment_cost, \
                k1_fix_o_and_m, k2_fix_o_and_m = default_dict.values()
            energy_price = energy_prices[fuel_type[technology]]

            heat_load = 1
            heating_energy_demand = 1
            if demand_type == 'heating':
                heating_energy_demand =  float(gfa) * (float(building_status_energy_factor[key])  * float(sp_heat) + float(sp_dhw))
                # heat load in kW
                heat_load = heating_energy_demand * factor
            else:
                cooling_energy_demand = float(gfa) * float(sp_cold)
                # cold load in kW
                cooling_load = float(cooling_energy_demand) * float(factor)
            specific_investment_cost = float(k1_specific_investment_cost) * float(heat_load)**float(k2_specific_investment_cost)
            fix_o_and_m = float(k1_fix_o_and_m) * (float(heat_load)**(float(k2_specific_investment_cost)))
            output[technology] = lcoh(heating_energy_demand, heat_load,
                  energy_price, specific_investment_cost, fix_o_and_m,
                  var_o_and_m, efficiency, r, lifetime)
        building_status[key] = output
        output = None
        output = dict()
    
    graphics = prj(building_status)
    return graphics
