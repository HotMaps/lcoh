import os,sys
from osgeo import gdal
import numpy as np, pandas as pd

import geopandas as gpd
from shapely.geometry import Point

path2data = os.path.split(os.path.abspath(__file__))[0]
path_nuts_code = os.path.join(path2data,"data_nuts_id_number.csv")

def get_nuts(nuts_code):
    nuts3 = nuts_code[:5]
    nuts2 = nuts_code[:4]
    nuts1 = nuts_code[:3]
    nuts0 = nuts_code[:2]
    return nuts3,nuts2,nuts1,nuts0

def raster_array(raster, dType=float, return_gt=False):
    ds = gdal.Open(raster)
    geo_transform = ds.GetGeoTransform()
    band1 = ds.GetRasterBand(1)
    arr = band1.ReadAsArray().astype(dType)
    ds = None
    if return_gt:
        return (arr, geo_transform),None  # 0..x,1...xres,3..y,5...yres
    else:
        return arr
    
def return_nuts_codes(path_to_raster):
    code_list = pd.read_csv(path_nuts_code)
    code_list = code_list.set_index("id")["nuts_code"]
    arr = raster_array(path_to_raster)
    arr = arr.astype(int)
    unique_val, counts = np.unique(arr[arr!=0] ,return_counts=True)
    # In case of region selection from several NUTS 3 areas, only the one with
    # highest number of elements is selected.
    code = unique_val[counts.argmax()]
    nuts_code = code_list[int(code)]
    nuts3,nuts2,nuts1,nuts0 = get_nuts(nuts_code)
    return (nuts0, nuts1, nuts2, nuts3) 


def get_temperature_and_radiation(point,target_epsg=4326,init_epsg=3035):
    os.environ['PROJ_LIB']  = os.path.join(os.path.dirname(sys.executable),"Library","share")
    p = gpd.GeoDataFrame([[Point(point)]], geometry='geometry', crs={'init': f'epsg:{init_epsg}'}, columns=['geometry'])   
    p = p.to_crs(epsg=target_epsg)
    lon = float(p.geometry.x)
    lat = float(p.geometry.y)
    req = f"https://re.jrc.ec.europa.eu/pvgis5/tmy.php?lat={lat}&lon={lon}"
    df = pd.read_csv(req,sep=",")
    radiation = dict(zip(range(1,8760+1),df[" Ghor"].values.tolist()))
    temperature = dict(zip(range(1,8760+1),df["Tair"].values.tolist())) 
    out = dict(temperature_t=temperature,radiation_t=radiation)
    return out


def get_max_heat_point(path_to_raster):
    out = raster_array(path_to_raster,return_gt=True)
    (arr,(x0,dx,_,y0,__,dy)) = out
    kx,ky = np.unravel_index(arr.argmax(), arr.shape)
    x = x0 + kx*dx
    y = y0 + ky*dy
    return (x,y)  


    

     
