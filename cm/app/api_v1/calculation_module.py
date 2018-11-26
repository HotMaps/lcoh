import os
import sys
import pandas as pd
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)
from osgeo import gdal

from ..helper import generate_output_file_tif
import my_calculation_module_directory.CM.CM_TUW2.run_cm as CM2
import my_calculation_module_directory.CM.CM_TUW19.run_cm as CM19
from my_calculation_module_directory.CM.CM_TUW1.read_raster import raster_array


verbose = True


def create_dataframe(input_dict):
    df = pd.DataFrame()
    for key in input_dict.keys():
        df[key] = input_dict[key]
    return df


""" Entry point of the calculation module function"""

#TODO: CM provider must "change this code"
#TODO: CM provider must "not change input_raster_selection,output_raster  1 raster input => 1 raster output"
#TODO: CM provider can "add all the parameters he needs to run his CM
#TODO: CM provider can "return as many indicators as he wants"
def calculation(output_directory, inputs_raster_selection,inputs_vector_selection, inputs_parameter_selection):

    """ def calculation()"""
    '''
    inputs:
        indicator_
        in_csv_
        in_shp_
        in_raster_

    Outputs:
        out_csv_
        out_shp_
        out_raster_

    '''
    # input parameters
    sector = inputs_parameter_selection["sector"]
    building_type = inputs_parameter_selection["building_type"]
    demand_type = inputs_parameter_selection["demand_type"]
    year = inputs_parameter_selection["year"]
    gfa = inputs_parameter_selection["gfa"]
    r = inputs_parameter_selection["r"]
    
    # input rows from CSV DB and create dataframe

    inputs_vector_selection = inputs_vector_selection["heating_technologies_eu28"]
    print('inputs_vector_selection****************************************************', inputs_vector_selection)
    in_df_tech_info = create_dataframe(inputs_vector_selection)

    print('in_df_tech_info', in_df_tech_info)
    if verbose:
        csv_path = path +  '/my_calculation_module_directory/CSVs'
        in_df_energy_price = pd.read_csv(csv_path + '/energy_price.csv')
        in_df_specific_demand = pd.read_csv(csv_path + '/AD.EURAC.Ave_useful_h&c_demand.csv')
    else:
        in_df_energy_price = create_dataframe(inputs_vector_selection['input_energy_price'])
        in_df_specific_demand = create_dataframe(inputs_vector_selection['space_heating_cooling_dhw_top-down'])
    
    # input raster
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
        in_raster_nuts_id_number = inputs_raster_selection['nuts_id_number']

    output_summary = CM2.main(sector, building_type, demand_type, year, gfa, r,
                              in_df_tech_info, in_df_energy_price,
                              in_df_specific_demand, in_raster_nuts_id_number)





    '''
    result = dict()
    result['name'] = 'CM District Heating Grid Investment'
    result["raster_layers"]=[{"name": "district heating coherent areas","path": out_raster_maxDHdem},
          {"name": "district heating coherent areas","path": out_raster_invest_Euro},
          {"name": "district heating coherent areas","path": out_raster_hdm_last_year},
          {"name": "district heating coherent areas","path": out_raster_dist_pipe_length},
          {"name": "district heating coherent areas","path": out_raster_coh_area_bool},
          {"name": "district heating coherent areas","path": out_raster_labels}]
    
    result["vector_layers"]=[{"name": "shapefile of coherent areas with their potential","path": out_shp_prelabel},
          {"name": "shapefile of coherent areas with their potential","path": out_shp_label},
          {"name": "shapefile of coherent areas with their potential","path": out_shp_edges},
          {"name": "shapefile of coherent areas with their potential","path": out_shp_nodes}]

    result["tabular"]=[{"name": "name of csv file","path": out_csv_solution}]
    result['indicator'] = output_summary

    return result
    '''
    

def colorizeMyOutputRaster(out_ds):
    ct = gdal.ColorTable()
    ct.SetColorEntry(0, (0,0,0,255))
    ct.SetColorEntry(1, (110,220,110,255))
    out_ds.SetColorTable(ct)
    return out_ds
