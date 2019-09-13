import urllib, shutil, os, sys
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np


# Helper functions for queries

"""
    This function downloads query results from the publicly accessible S3 bucket
    and saves them to the /www/ folder as <query id>.csv
   
    Input: The URL of the data on AWS (from the Athena link)
    Returns: Pandas dataframe with query results 
"""
def load_dataframe_from_s3(link):
    base_url = "https://hot-aws-workshop.s3.us-east-2.amazonaws.com/"
    if len(link)== 36:
        query_id = link
    else:
        query_id = link.split('/')[-2]
    
    if os.path.isfile("/www/"+query_id+".csv"):
        sys.stderr.write("Found file locally... ")
    else:
        sys.stderr.write("Downloading from S3... ")
        with urllib.request.urlopen(base_url + query_id + ".csv") as response, open("/www/"+query_id+".csv", 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        sys.stderr.write("Query results saved to: \n"+"/www/"+query_id+".csv\n")
    
    sys.stderr.write("Creating dataframe... ")
    d = pd.read_csv('/www/'+query_id+".csv")
    sys.stderr.write("done.  Found {:,} rows".format(len(d)))
    return d

"""
    This function takes a string from Athena that represents a Map and returns the Python
    dictionary equivalent
"""
def string_to_dict(string):
    if type(string)==str:
        arr = string[1:-1].split("=")
        d = dict()
        for k, v in zip(arr[:-1], arr[1:]):
            d[k] = v
        return d
    elif type(string)==dict:
        return string
    
def make_grid(length=0.1,width=0.1):
    xmin,ymin,xmax,ymax = points.total_bounds

    length = 0.1
    wide = 0.1

    cols = list(np.arange(int(np.floor(xmin)), int(np.ceil(xmax)), wide))
    rows = list(np.arange(int(np.floor(ymin)), int(np.ceil(ymax)), length))
    rows.reverse()

    polygons = []
    ids = []; count=0
    for x in cols:
        for y in rows:
            count = count + 1
            ids.append(count)
            polygons.append( Polygon([(x,y), (x+wide, y), (x+wide, y-length), (x, y-length)]) )

    return gpd.GeoDataFrame({'geometry':polygons, 'PolyID':ids})