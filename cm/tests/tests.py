import unittest
from werkzeug.exceptions import NotFound
from app import create_app
import os.path
from shutil import copyfile
from .test_client import TestClient
import pandas as pd
import numpy as np
UPLOAD_DIRECTORY = '/var/hotmaps/cm_files_uploaded'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
    os.chmod(UPLOAD_DIRECTORY, 0o777)


class TestAPI(unittest.TestCase):


    def setUp(self):
        self.app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.client = TestClient(self.app,)

    def tearDown(self):

        self.ctx.pop()


    def test_compute(self):
        raster_file_path = "tests/data/raster_for_test.tif"
        json_file_test = "tests/data/heat_tec_EU28_fixed2.text.txt"
        
        # simulate copy from HTAPI to CM
        save_path = UPLOAD_DIRECTORY+"/raster_for_test.tif"
        copyfile(raster_file_path, save_path)
        inputs_vector_selection = {}
        inputs_raster_selection = {}
        inputs_parameter_selection = {}
        inputs_raster_selection["heat_tot_curr_density"]  = save_path
        import json
        with open(json_file_test) as json_data:
            d=json.load(json_data)
        json_data.close()
        inputs_vector_selection['heating_technologies_eu28'] = d
        inputs_parameter_selection["sector"] = "residential"
        inputs_parameter_selection["building_type"] = "new SFH"
        inputs_parameter_selection["demand_type"] = "heating"
        inputs_parameter_selection["year"] = 2015
        inputs_parameter_selection["gfa"] = 100
        inputs_parameter_selection["r"] = 0.05
        df = None
        # register the calculation module a
        payload = {"inputs_raster_selection": inputs_raster_selection,
                   "inputs_vector_selection": inputs_vector_selection,
                   "inputs_parameter_selection": inputs_parameter_selection}


        rv, json = self.client.post('computation-module/compute/', data=payload)

        self.assertTrue(rv.status_code == 200)


