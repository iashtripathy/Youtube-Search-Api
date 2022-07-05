from flask import Flask
import pymongo
import os, sys
from requests import get
import asyncio
from json import loads

import datetime
import random
import time
import threading




app = Flask(__name__)



# Gets the MongoDB URI from .env file
MongoURI = os.environ.get('MONGODB_URI', None)

# Setting multiple API Keys
TotalAPIKeys = int(os.environ.get('TotalAPIKeys', 1))

if MongoURI is None:
    sys.exit("\n * MongoDB URI not provided.\n")


client = pymongo.MongoClient(MongoURI)

# mydb is my Database
db = client.mydb

# metaInfo is the Collection where info about videos are stored
collection = db.metaInfo




# Template to convert time format
@app.template_filter()
def fmdatetime(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")


# Function to insert data into db
def insert_data(fetched_data):


    print('inserting data')

    
    try:
        for data in fetched_data:
            
            # Key to find if data is present or not.
            print("Fetched video Id is : ",data["id"]["videoId"])
            key = {'videoId': data["id"]["videoId"]}

            meta_data = {
                "videoId": data["id"]["videoId"],
                "videoTitle": data["snippet"]["title"],
                "description": data["snippet"]["description"],
                "publishedAt": data["snippet"]["publishedAt"],
                "thumbnailUrl": data["snippet"]["thumbnails"]["medium"]["url"],
                "channelName": data["snippet"]["channelTitle"]
            }

            # Checks videoId already present or not.
            collection.update(key, meta_data, upsert=True)
            
            
    except Exception as e:
        print(e)

# Asynchronous function call for Fetching data from Youtube API
async def fetch_data_from_ytApi():

    # Selects a random api from n number of api keys given in .env file 
    i = str(random.randint(1, TotalAPIKeys))
    ytAPIKey = os.environ.get(f'YTAPIKey{i}', None)

    # Simple check to handle no api's
    if ytAPIKey is None:
        sys.exit("\n * Please provide the Youtube API Key.\n")

    
    # Default search query to get Football data 
    query = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&order=date&q=football&key={ytAPIKey}"

    
    
    while True:
        start = time.time()
        try:
            res = get(query)
        except Exception as e:
            print(e)
        
        # Checks if data is fetched or not
        if res.status_code == 200:
            print(res)
            res = res.content.decode("utf-8")
            print('Received data from YT')
            fetched_data = loads(res)
            insert_data(fetched_data["items"])
        
        else:
            # Please see line 26-30 for details
            i = str(random.randint(1, TotalAPIKeys))
            ytAPIKey = os.environ.get(f'YTAPIKey{i}', None)
            query = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&order=date&q=football&key={ytAPIKey}"
        end = time.time()
        print()
        print("It took {} second".format(end-start))
        print()
        await asyncio.sleep(10)




# Function for initialising Async Loop
#asyncio.run(fetch_data_from_ytApi())

# Function for initialising Async Loop
def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_data_from_ytApi())

# Puts the get request in background 
loop = asyncio.get_event_loop()
#loop.run_until_complete(fetch_data_from_ytApi())
t = threading.Thread(target=loop_in_thread, args=(loop,))

# Below line is to make the thread daemon thread so that it responds to keyboard interrupt
t.daemon = True
t.start()




# imports views from views.py
from app import views

if __name__ == "__main__":
    app.run();

