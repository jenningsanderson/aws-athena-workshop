import urllib, shutil, os, sys
import pandas as pd

# Helper functions for queries

"""
    This function downloads query results from the publicly accessible S3 bucket
    and saves them to the data/ folder as <query id>.csv
   
    Input: The URL of the data on AWS (from the Athena link)
    Returns: Pandas dataframe with query results 
"""
def load_dataframe_from_s3(link):
    base_url = "https://2019-hotsummit-aws-workshop-us2.s3.us-east-2.amazonaws.com/"
    if len(link)== 36:
        query_id = link
    else:
        query_id = link.split('/')[-2]
    
    if os.path.isfile("data/"+query_id+".csv"):
        sys.stderr.write("Found file locally... ")
    else:
        sys.stderr.write("Downloading from S3... ")
        with urllib.request.urlopen(base_url + query_id + ".csv") as response, open("data/"+query_id+".csv", 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        sys.stderr.write("Query results saved to: \n"+"data/"+query_id+".csv\n")
    
    sys.stderr.write("Creating dataframe... ")
    d = pd.read_csv('data/'+query_id+".csv")
    sys.stderr.write("done.  Found {:,} rows".format(len(d)))
    return d