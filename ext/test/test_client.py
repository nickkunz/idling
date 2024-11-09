## libraries
import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.text_format import MessageToString

## define params
url = "http://127.0.0.1:8080/extract"
data = "./ext/test/data/test_data.txt"

## test local server
response = requests.get(url)
if response.status_code == 200:

    ## parse protobuf response
    vehicle_positions = gtfs_realtime_pb2.FeedMessage()
    vehicle_positions.ParseFromString(response.content)
    
    ## save data
    with open(data, "w") as file:
        file.write(MessageToString(vehicle_positions))
    print(f"Human readable response payload saved in the following path: {data}")

## error handling
else:
    print("Failed to retrieve payload:", response.status_code, response.text)