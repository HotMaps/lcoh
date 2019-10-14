
from ..helper import generate_output_file_tif, create_zip_shapefiles
from ..constant import CM_NAME
from .my_calculation_module_directory import decentral_heating_supply_standalone as dhs
from .my_calculation_module_directory import hotmaps_api
""" Entry point of the calculation module function"""

#TODO: CM provider must "change this code"
#TODO: CM provider must "not change input_raster_selection,output_raster  1 raster input => 1 raster output"
#TODO: CM provider can "add all the parameters he needs to run his CM
#TODO: CM provider can "return as many indicators as he wants"    
def calculation(output_directory, inputs_raster_selection, inputs_parameter_selection):
    inputs,ok,message = hotmaps_api.get_inputs( inputs_raster_selection, inputs_parameter_selection)
    if ok:
        results,inputs2 =  dhs.main(*inputs)
        indicators,graphics = hotmaps_api.generate_output(results,inputs,inputs2)
    else:
        graphics = []
        indicators = [dict(unit="",name="Errors",value=message)]

    result = dict()
    result['name'] = CM_NAME
    result['indicator'] = indicators
    result['graphics'] = graphics
#    result['vector_layers'] = []
#    result['raster_layers'] = [] 
    
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result) 
   
    
    result = dict()
    result["name"] = "Test"
    result["indicator"] = [{"unit": "Einheit", "name": "Testindicator", "value" : "42"},
                          {"unit": "Einheit2", "name": "22Testindicator", "value" : "176"},
                           {'name': 'point in value', 'unit': 'hh', 'value': '.'},
                           {'name': 'empty value', 'unit': 'hh', 'value': ''},
                           {'name': 'empty space in unit', 'unit': ' ', 'value': '0'},
                           {'name': 'empty unit', 'unit': '', 'value': '0'}] 
    result["indicator"].append( {'name': 'nuts_code', 'unit': 'hh', 'value': '130'})

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result) 

    
    return result



    