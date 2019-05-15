import requests
import time
import uuid

from pymongo import MongoClient

from datetime import datetime
import random
import math

client = MongoClient('mongodb://localhost:27017')
db = client["sensorDB"]
mycol = db["sensorCollection"]

sensor_URL = 'http://ec2-3-81-127-12.compute-1.amazonaws.com:8080/getAllSensor'
mongo_URL = 'http://54.67.113.246:8080/save'

# Declare class for clusterNode
class ClusterNode:
    def __init__(self, networkID, clusterID, lat, lon):
        self.networkID = networkID
        self.clusterID = clusterID
        self.lat = lat
        self.lon = lon


# Declare class for sensor node
class SensorNode:
    def __init__(self, clusterID, sensorNodeID, lat, lon):
        self.clusterID = clusterID
        self.sensorNodeID = sensorNodeID
        self.lat = lat
        self.lon = lon


# Declare sensor class
class Sensor:
    def __init__(self, sensorid, sensorType, status):
        self.sensorID = sensorid
        self.sensorType = sensorType
        self.sensorStatus = status

    def checkSensorStatus(self):
        if self.sensorStatus == "Active":
            #print("Sensor is active: ", self.sensorID)
            return True

    def generate_temperature_data(self, id, currtime):
            x = math.sin(((currtime / 86400) * 36) * math.pi * 2) * 15 + 65
            db.mycol.insert_one({"Sensor ID": id, "Timestamp": datetime.now(), "Sensor Value": x})

    def generate_water_data(self, id, currtime):
            choice_list = [1, 0]
            x = math.sin(((currtime / 86400) * 36) * math.pi * 2) * 0.5 + 0.5
            db.mycol.insert_one({"Sensor ID": id, "Timestamp": datetime.now(), "Sensor Value": round(x)})

    def generate_ph_data(self, id, currtime):
            x = math.sin(((currtime / 86400) / 30) * math.pi * 2) * 1 + 6
            db.mycol.insert_one({"Sensor ID": id, "Timestamp": datetime.now(), "Sensor Value": x})


if __name__ == '__main__':
    # app.run()
    r = requests.get(sensor_URL).json()
    print(r)
    sensorObj=[]
    for item in r:
        sensorL = []
        for k, v in item.items():
            sensorL.append(v)
        my_sensor = Sensor(sensorL[0], sensorL[1], sensorL[2])
        sensorObj.append(my_sensor)
    #print(sensorObj)
    print("Simulator On")
    current_time_in_sec = time.time()
    while time.time() <= current_time_in_sec + 60:
        for item in sensorObj:
            if item.sensorStatus == "Active":
                if item.sensorType == "Temperature":
                    item.generate_temperature_data(item.sensorID, time.time())
                elif item.sensorType == "Water":
                    item.generate_water_data(item.sensorID, time.time())
                elif item.sensorType == "PH":
                    item.generate_ph_data(item.sensorID, time.time())
        time.sleep(5)
    print("Simulator Off")
    data_list = []
    mydoc = db.mycol.find({}, {"_id": 0})

    for x in mydoc:
        data_list.append(x)
    #print(data_list[0])
    print("Sending Data....")
    for item in data_list:
        #print(item.get('Sensor ID'), item.get("Timestamp"), item.get("Sensor Value"))
        requests.post(mongo_URL, data={'sensor_id': item.get('Sensor ID'),
                                       'd': item.get("Timestamp"), 'value': item.get("Sensor Value")})
    print("Done")
    data_list.clear()
    db.mycol.drop()
    


