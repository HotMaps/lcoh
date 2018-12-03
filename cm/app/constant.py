
CELERY_BROKER_URL_DOCKER = 'amqp://admin:mypass@rabbit:5672/'
CELERY_BROKER_URL_LOCAL = 'amqp://localhost/'

CELERY_BROKER_URL = CELERY_BROKER_URL_DOCKER
CM_REGISTER_Q = 'rpc_queue_CM_register' # Do no change this value

CM_NAME = 'Levelozed cost of heat'
RPC_CM_ALIVE= 'rpc_queue_CM_ALIVE' # Do no change this value
RPC_Q = 'rpc_queue_CM_compute' # Do no change this value
CM_ID = 5 # CM_ID is defined by the enegy research center of Martigny (CREM)
PORT_LOCAL = int('500' + str(CM_ID))
PORT_DOCKER = 80
PORT = PORT_DOCKER
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
      'input_value': ["service", "residential"],
      'input_unit': '',
      'input_min': '',
      'input_max': '',
      'cm_id': CM_ID
      },
     {
      'input_name': 'Building type',
      'input_type': 'select',
      'input_parameter_name': "building_type",
      'input_value': ["service",
                      "new SFH",
                      "new MFH"],
      'input_unit': '',
      'input_min': '',
      'input_max': '',
      'cm_id': CM_ID
      },
     {
      'input_name': 'Demand type',
      'input_type': 'select',
      'input_parameter_name': 'demand_type',
      'input_value': '["heating", "cooling"]',
      'input_unit': '',
      'input_min': '',
      'input_max': '',
      'cm_id': CM_ID
      },
     {
      'input_name': 'Year',
      'input_type': 'select',
      'input_parameter_name': 'year',
      'input_value': ["2015", "2020", "2030", "2050"],
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
    "layers_needed": [
            "heat_tot_curr_density"
            ],
    "type_layer_needed": [
            "heat"
            ],
    "vectors_needed": [
        "heating_technologies_eu28",

    ],
    "cm_url": "Do not add something",
    "cm_description": "this computation module calculates the levelized cost of heat/cold",
    "cm_id": CM_ID,
    'inputs_calculation_module': INPUTS_CALCULATION_MODULE
}
