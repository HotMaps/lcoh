import unittest
from werkzeug.exceptions import NotFound
from app import create_app
import os.path
from shutil import copyfile
from .test_client import TestClient
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
        for btype in [   'Multifamily houses',
                           'Single family- Terraced houses',
                           'Appartment blocks',
                           'Trade',
                           'Other non-residential buildings',
                           'Hotels and Restaurants',
                           'Offices',
                           'Health',
                           'Education']:
            
            for bage in [   'Before 1945',
                           '1945 - 1969',
                           '1970 - 1979',
                           '1980 - 1989',
                           '1990 - 1999',
                           '2000 - 2010',
                           'Post 2010']:
                for year in ['2015', '2020', '2030', '2050']:
                    
                    print("#"*100)
                    print(f"Testing with: year: {year}, btype: {btype}, bage: {bage}")
                    
                    raster_file_path = 'tests/data/nuts_id.tif'
                    # simulate copy from HTAPI to CM
                    save_path = UPLOAD_DIRECTORY+"/raster_for_test.tif"
                    copyfile(raster_file_path, save_path)
            
                    inputs_raster_selection = {}
                    inputs_parameter_selection = {}
                    inputs_vector_selection = {}
                    inputs_raster_selection["nuts_id_number"]  = save_path
                    
                    inputs_parameter_selection["sav"] = "10" # savings in % [0.1,99.9]
                    inputs_parameter_selection["gfa"] = "150"  # Gross Floor Area in m² 
                    inputs_parameter_selection["year"] = year # int
                    inputs_parameter_selection["r"] = "0.01" # interest rate
                    inputs_parameter_selection["bage"] = bage # None for mean value
                    inputs_parameter_selection["btype"] = btype # "Total" for mean value
                    # emission factors
                    inputs_parameter_selection["ef_elec"] = 0.270224 
                    inputs_parameter_selection["ef_oil"] = 0.2664 
                    inputs_parameter_selection["ef_biomas"] = 0.312 
                    inputs_parameter_selection["ef_gas"] = 0.20124 
            
                    # register the calculation module a
                    payload = {"inputs_raster_selection": inputs_raster_selection,
                               "inputs_parameter_selection": inputs_parameter_selection,
                               "inputs_vector_selection": inputs_vector_selection}
            
            
                    rv, json = self.client.post('computation-module/compute/', data=payload)
            
                    self.assertTrue(rv.status_code == 200)


