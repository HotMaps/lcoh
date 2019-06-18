
CELERY_BROKER_URL_DOCKER = 'amqp://admin:mypass@rabbit:5672/'
CELERY_BROKER_URL_LOCAL = 'amqp://localhost/'


CM_REGISTER_Q = 'rpc_queue_CM_register' # Do no change this value

CM_NAME = 'CM - Decentral heating supply'
RPC_CM_ALIVE= 'rpc_queue_CM_ALIVE' # Do no change this value
RPC_Q = 'rpc_queue_CM_compute' # Do no change this value
CM_ID = 5 # CM_ID is defined by the enegy research center of Martigny (CREM)
PORT_LOCAL = int('500' + str(CM_ID))
PORT_DOCKER = 80
#TODO:**********************************************************
CELERY_BROKER_URL = CELERY_BROKER_URL_LOCAL
PORT = PORT_LOCAL
#TODO:**********************************************************
TRANFER_PROTOCOLE ='http://'
INPUTS_CALCULATION_MODULE = [

    {'input_name': 'Gross floor area',
     'input_type': 'input',
     'input_parameter_name': 'gfa',
     'input_value': 100,
     'input_unit': 'm2',
     'input_min': 1,
     'input_max': 10000,
     'cm_id': CM_ID
     },
    {'input_name': 'Interest rate',
     'input_type': 'input',
     'input_parameter_name': 'r',
     'input_value': 0.05,
     'input_unit': '',
     'input_min': 0,
     'input_max': 1,
     'cm_id': CM_ID
     },
     {
      'input_name': 'Sector',
      'input_type': 'radio',
      'input_parameter_name': 'sector',
      'input_value': [
              "residential",
              # "service"
              ],
      'input_unit': '',
      'input_min': '',
      'input_max': '',
      'cm_id': CM_ID
      },
     {
      'input_name': 'Building type',
      'input_type': 'select',
      'input_parameter_name': "building_type",
      'input_value': ["Single family house",
                      "Multi family house",
                      # "Service sector (average)"
                      ],
      'input_unit': '',
      'input_min': '',
      'input_max': '',
      'cm_id': CM_ID
      },
      {
      'input_name': 'Building class',
      'input_type': 'select',
      'input_parameter_name': "building_class",
      'input_value': ["Existing building",
                      "Renovated building",
                      "New building"
                      ],
      'input_unit': '',
      'input_min': '',
      'input_max': '',
      'cm_id': CM_ID
      },
     {
      'input_name': 'Demand type',
      'input_type': 'select',
      'input_parameter_name': 'demand_type',
      'input_value': '["heating"]',
      'input_unit': '',
      'input_min': '',
      'input_max': '',
      'cm_id': CM_ID
      },
     {
      'input_name': 'Year',
      'input_type': 'select',
      'input_parameter_name': 'year',
      'input_value': ["2015"],
      'input_unit': '',
      'input_min': '',
      'input_max': '',
      'cm_id': CM_ID
      },
]


SIGNATURE = {
    "category": "Buildings",
    "authorized_scale":["NUTS 2", "NUTS 3","LAU 2","Hectare"],
    "cm_name": CM_NAME,
    "description_link": "",
    "layers_needed": [
            "nuts_id_number"
            ],
    "type_layer_needed": [
            "nuts_id_number"
            ],
    "vectors_needed": [
        "heating_technologies_eu28",

    ],
    "cm_url": "Do not add something",
    "cm_description": "This calclulation module calculates the levelized " \
    "cost of heat (LCOH) for the various technologies. The results will be shown " \
    "for the selected building class, building and new building. \n\nNote: In the current " \
    "version, dummy input values have been used!",
    "cm_id": CM_ID,
    'inputs_calculation_module': INPUTS_CALCULATION_MODULE
}
