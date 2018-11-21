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
        raster_file_path = 'tests/data/raster_for_test.tif'
        csv_file_path = 'tests/data/technologies.csv'
        
        # simulate copy from HTAPI to CM
        save_path = UPLOAD_DIRECTORY+"/raster_for_test.tif"
        copyfile(raster_file_path, save_path)
        df = pd.read_csv(csv_file_path)
        inputs_csv_selection = {}
        inputs_raster_selection = {}
        inputs_parameter_selection = {}
        inputs_raster_selection["heat_tot_curr_density"]  = save_path

        for column in df.columns:
            '''
            temp = []
            obj = df[column].values
            for item in obj:
                if type(item) == str:
                    temp.append(item)
                else:
                    if np.isnan(item):
                        temp.append(0)
                    else:
                        temp.append(item)
            '''        
            inputs_csv_selection[column] = list(df[column])
            
        df = None
        inputs_parameter_selection["sector"] = 'residential'
        inputs_parameter_selection["building_type"] = 'new SFH'
        inputs_parameter_selection["demand_type"] = 'heating'
        inputs_parameter_selection["year"] = 2015
        inputs_parameter_selection["gfa"] = 100
        inputs_parameter_selection["r"] = 0.05
        
        # register the calculation module a
        payload = {"inputs_raster_selection": inputs_raster_selection,
                   "inputs_csv_selection": inputs_csv_selection,
                   "inputs_parameter_selection": inputs_parameter_selection}


        rv, json = self.client.post('computation-module/compute/', data=payload)

        self.assertTrue(rv.status_code == 200)


