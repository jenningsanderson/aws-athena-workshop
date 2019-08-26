import urllib, shutil
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

    with urllib.request.urlopen(base_url + query_id + ".csv") as response, open("data/"+query_id+".csv", 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    print("Query results saved to: \n"+"data/"+query_id+".csv", end="")
    
    return pd.read_csv('data/'+query_id+".csv")