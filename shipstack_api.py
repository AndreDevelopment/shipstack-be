# API endpoints
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from service import get_clusters
import uvicorn
import json
import pandas as pd


app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://localhost:5174",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Models --------------------------------------
class ClusterRequest(BaseModel):
    desintations:list
    origin_point:str

class Cluster(BaseModel):
    groupName:str
    locations:list


# Endpoints -----------------------------------
@app.get("/")
def root():
    pass

@app.post("/uploadAddr")
def upload_addresses(cluster_req:dict):
    epsilonRadius = float(cluster_req["epsilon"])  # extracted radius
    print(cluster_req)
    dests= cluster_req["destinations"]
    clusters = get_clusters(cluster_req["origin"],dests, epsilonRadius)
    clusters = format_cluster_array(clusters)
    
    # json_clusters= json.dumps(clusters)
    # print(json_clusters) 
    return clusters


def format_cluster_array(clusters):
    
    result = []
    for key in clusters.keys():
        result.append({         
            'groupName':str(key),
            'locations':clusters[key]
        })
    
    result = json.dumps(result)
    print(result)
    return result