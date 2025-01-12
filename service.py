from sklearn.cluster import DBSCAN
import numpy as np
import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('SECRET_KEY')
gmaps = googlemaps.Client(key=key)


# Test Data
# origin = 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
# New York, NY|Los Angeles, CA|Chicago, IL|Houston, TX|Miami, FL

def calculate_distances(origin, destinations):
    # API results
    results = gmaps.distance_matrix(origin, destinations, mode='driving')
    # Foramtting results
    distances_wrt_origin = []
    for i, dest in enumerate(destinations):
        info = results["rows"][0]["elements"][i]
        distances_wrt_origin.append({
            'destination': dest,
            'distance_meters': info['distance']['value'],
            'duration_text': info['duration']['text']
        })
        
    return distances_wrt_origin


def get_clusters(origin, destinations, epsilon):
    distances_wrt_origin = calculate_distances(origin,destinations)
    distances = np.array([[d['distance_meters']] for d in distances_wrt_origin])
    
    print(f"distances: {distances}")

    epsilon = float(epsilon * 1000)
    min_samples = 2  # Minimum points to form a cluster

    db = DBSCAN(eps=epsilon, min_samples=min_samples, metric='euclidean').fit(distances)
    clusters = {}
    labels = db.labels_

    distance_to_dest_map = {d['distance_meters']: d['destination'] for d in distances_wrt_origin}
    
    

    for label, distance in zip(labels, distances):
        if label not in clusters:
            clusters[int(label)] = []
        # Use the distance to find the corresponding destination name (destinaiton is the key)
        destination_name = distance_to_dest_map.get(distance[0])
        clusters[int(label)].append(destination_name)

        # Pretty Print clusters
        # print("Clustered Destinations:")
        # for cluster_id, destinations in clusters.items():
        #     if cluster_id == -1:
        #         print(f"Cluster {cluster_id} (outliers):")
        #         for destination in destinations:
        #             print(f"  {destination}")
        #     else:
        #         print(f"Cluster {cluster_id}:")
        #         for destination in destinations:
        #             print(f"  {destination}")
        
    return clusters


        


