
CELERY_BROKER_URL_DOCKER = 'amqp://admin:mypass@rabbit:5672/'
CELERY_BROKER_URL_LOCAL = 'amqp://localhost/'


CM_REGISTER_Q = 'rpc_queue_CM_register' # Do no change this value

CM_NAME = 'CM - Decentral heating supply'
RPC_CM_ALIVE= 'rpc_queue_CM_ALIVE' # Do no change this value
RPC_Q = 'rpc_queue_CM_compute' # Do no change this value
CM_ID = 5 # CM_ID is defined by the enegy research center of Martigny (CREM)
PORT_LOCAL = int('500' + str(CM_ID))
PORT_DOCKER = 80

#TODO ********************setup this URL depending on which version you are running***************************

CELERY_BROKER_URL = CELERY_BROKER_URL_DOCKER
PORT = PORT_DOCKER

#TODO ********************setup this URL depending on which version you are running***************************

TRANFER_PROTOCOLE ='http://'
INPUTS_CALCULATION_MODULE = [ 
         {'cm_id': CM_ID,
          'input_max': '',
          'input_min': '',
          'input_name': 'Buidling age',
          'input_parameter_name': 'bage',
          'input_type': 'select',
          'input_unit': '',
          'input_value': ['Before 1945',
                          '1945 - 1969',
                          '1970 - 1979',
                          '1980 - 1989',
                          '1990 - 1999',
                          '2000 - 2010',
                          'Post 2010']},
         {'cm_id': CM_ID,
          'input_max': '1.0',
          'input_min': '0.0',
          'input_name': 'Interest rate',
          'input_parameter_name': 'r',
          'input_type': 'input',
          'input_unit': '',
          'input_value': '0.03'},
         {'cm_id': CM_ID,
          'input_min': '100e-100',
          'input_max': '100e100',
          'input_name': 'Gross Floor Area',
          'input_parameter_name': 'gfa',
          'input_type': 'input',
          'input_unit': 'm2',
          'input_value': '1000'},
         {'cm_id': CM_ID,
          'input_max': '',
          'input_min': '',
          'input_name': 'Building category',
          'input_parameter_name': 'btype',
          'input_type': 'select',
          'input_unit': '',
          'input_value': ['Multifamily houses',
                          'Single family- Terraced houses',
                          'Appartment blocks',
                          'Trade',
                          'Other non-residential buildings',
                          'Hotels and Restaurants',
                          'Offices',
                          'Health',
                          'Education']},
         {'cm_id': CM_ID,
          'input_max': '',
          'input_min': '',
          'input_name': 'Year',
          'input_parameter_name': 'year',
          'input_type': 'select',
          'input_unit': '',
          'input_value': ['2015', '2020', '2030', '2050']},
         {'cm_id': CM_ID,
          'input_max': '99.9',
          'input_min': '0',
          'input_name': 'Savings for space heating ',
          'input_parameter_name': 'sav',
          'input_type': 'input',
          'input_unit': '%',
          'input_value': '0'},
         {'cm_id': CM_ID,
          'input_priority': '1',
		  'input_min': '-100e100',
          'input_max': '100e100',
          'input_name': 'Emission factor - Electricity ',
          'input_parameter_name': 'ef_elec',
          'input_type': 'input',
          'input_unit': 'tCO2/MWh',
          'input_value': '0.270224'},
         {'cm_id': CM_ID,
          'input_priority': '1',
		  'input_min': '-100e100',
          'input_max': '100e100',
          'input_name': 'Emission factor - Light fuel oil ',
          'input_parameter_name': 'ef_oil',
          'input_type': 'input',
          'input_unit': 'tCO2/MWh',
          'input_value': '0.2664'},
         {'cm_id': CM_ID,
          'input_priority': '1',
		 'input_min': '-100e100',
          'input_max': '100e100',
          'input_name': 'Emission factor - Biomass solid',
          'input_parameter_name': 'ef_biomas',
          'input_type': 'input',
          'input_unit': 'tCO2/MWh',
          'input_value': '0.312'},
         {'cm_id': CM_ID,
          'input_priority': '1',
		  'input_min': '-100e100',
          'input_max': '100e100',
          'input_name': 'Emission factor - Natural gas',
          'input_parameter_name': 'ef_gas',
          'input_type': 'input',
          'input_unit': 'tCO2/MWh',
          'input_value': '0.20124',}]




SIGNATURE = {

    "category": "Supply",
    "cm_name": CM_NAME,
    "layers_needed": [
        "nuts_id_number",
    ],
    "type_layer_needed": [
        {"type": "nuts_id_number", "description": "You can choose the layer of type 'heat'."}
    ],
    "vectors_needed": [

    ],
    "cm_url": "Do not add something",
    "cm_description": """This calclulation module calculates the levelized cost 
    of heat (LCOH) for various technologies to supply a user definded building""",
    "cm_id": CM_ID,
    "wiki_url":"https://wiki.hotmaps.eu/en/CM-Decentral-heating-supply",
    'inputs_calculation_module': INPUTS_CALCULATION_MODULE
}
