import os
import sys
import pandas as pd
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)
from osgeo import gdal
#from ..exceptions import ValidationError,EmptyRasterError
#from ..helper import generate_output_file_tif
import my_calculation_module_directory.CM.CM_TUW2.run_cm as CM2
#import my_calculation_module_directory.CM.CM_TUW19.run_cm as CM19
#from my_calculation_module_directory.CM.CM_TUW1.read_raster import raster_array
verbose = True


def create_dataframe(input_dict):
    temp = '%s' %input_dict
    temp = temp.replace("\'","\"")
    df = pd.read_json(temp, orient='records')
    return df


def calculation(output_directory, inputs_raster_selection,inputs_vector_selection, inputs_parameter_selection):
    """ def calculation()"""
    '''
    inputs:


        sector: residential or service
        building type: single family or multi family house
        building class: existing, renovated or new building
        demand type: heating or cooling
        year: year to be calculated for
        gfa: gross floor area of the building
        r: interest rate
        in_df_tech_info: input csv including the technologies and their parameters
        in_df_energy_price: energy carrier price
        in_df_specific_demand: specific heating or cooling demand in a country
        

    Outputs:
        are in form of graphs and indicators
    '''
    # ***************************** input parameters**************************

    sector = inputs_parameter_selection["sector"]
    building_type = inputs_parameter_selection["building_type"]
    building_class = inputs_parameter_selection["building_class"]
    demand_type = inputs_parameter_selection["demand_type"]
    year = inputs_parameter_selection["year"]
    gfa = inputs_parameter_selection["gfa"]
    r = inputs_parameter_selection["r"]


    # *********** # input rows from CSV DB and create dataframe***************
    in_df_tech_info = create_dataframe(inputs_vector_selection['heating_technologies_eu28'])
    if verbose:
        csv_path = path +  '/my_calculation_module_directory/CSVs'
        in_df_energy_price = pd.read_csv(csv_path + '/AD.TUW2_fuel_costs.csv')
        in_df_specific_demand = pd.read_csv(csv_path + '/AD.EURAC.Ave_useful_h&c_demand.csv')

    else:
        in_df_energy_price = create_dataframe(inputs_vector_selection['input_energy_price'])
        in_df_specific_demand = create_dataframe(inputs_vector_selection['space_heating_cooling_dhw_top-down'])
    

    # input raster
    '''
    if verbose:
        in_raster_nuts_id_number = generate_output_file_tif(output_directory)
        in_raster_hdm = inputs_raster_selection['heat_tot_curr_density']
        raster_path = path +  '/my_calculation_module_directory/Rasters/nuts_id_number.tif'
        from osgeo import gdal
        arr, gt = raster_array(in_raster_hdm, return_gt=True)
        ds1 = gdal.Open(raster_path)
        gt1 = ds1.GetGeoTransform()
        x_off = (gt[0] - gt1[0])/100
        y_off = (gt1[3] - gt[3])/100
        x_dim, y_dim = arr.shape
        arr_new = ds1.ReadAsArray(x_off,y_off, y_dim, x_dim)
        ds1 = None
        # set all pixels out of the selection zone to zero
        arr_new = arr_new * arr.astype(bool).astype(int)

        CM19.main(in_raster_nuts_id_number, gt, 'int16', arr_new)
    else:
    '''
    in_raster_nuts_id_number = inputs_raster_selection['nuts_id_number']
    graphics, indictor_list = CM2.main(sector, building_type, building_class,
                                       demand_type, year, gfa, r,
                                       in_df_tech_info, in_df_energy_price,
                                       in_df_specific_demand,
                                       in_raster_nuts_id_number)
    result = dict()
    result['name'] = 'CM Levelized Cost of Heat'
    result['indicator'] = indictor_list
    result['graphics'] = graphics
    return result
    

def colorizeMyOutputRaster(out_ds):
    ct = gdal.ColorTable()
    ct.SetColorEntry(0, (0,0,0,255))
    ct.SetColorEntry(1, (110,220,110,255))
    out_ds.SetColorTable(ct)
    return out_ds