from flask import Flask
from flask import request
from flask import render_template
import uuid
from flask_pymongo import PyMongo, MongoClient
import datetime
import random
#import mysql.connector

from flask_mysqldb import MySQL


client = MongoClient('mongodb://localhost:27017')
db = client["sensorDB"]
mycol = db["sensorCollection"]

'''
cnx = mysql.connector.connect(user='root', password='rootpass',
                              host='localhost:3036',
                              database='sensorDB')
cursor = cnx.cursor()
'''
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
    def __init__(self, sensorNodeID, sensorType, numOfSensor):
        self.sensorNodeID = sensorNodeID
        self.sensorType = sensorType
        self.numOfSensor = numOfSensor

    def createSensorID(self, num):
        sensorID = [str(uuid.uuid4().hex) for i in range(0, num)]
        print(sensorID)
        return sensorID


    def set_sensor_status(self, sensorID, status):
        #return status
        statusList =[status for i in range(0, len(sensorID))]
        print(statusList)
        return statusList


    def generate_mongo_sensor_data(self, sensorID, type, status):
        # insert sensor data to db
        ##for elem in sensorID:
        #while status =="on":
        for i in range(len(sensorID)):
            db.mycol.insert({"Sensor ID": sensorID[i], "Sensor Type": type, "Sensor Status": status, "Timestamp":
                datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).isoformat(),
                             "Sensor Value": random.randint(65, 80)})
            #db.mycol.insert({"Sensor Type": type})
            #db.mycol.insert({"Timestamp": datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).isoformat()})
            #db.mycol.insert({"Sensor Value": random.randint(32, 108)})
        print("Mongo Data added!!!")

    def generate_mysql_sensor_data(self, sensorID, stype, status):
        cur = mysql.connection.cursor()
        for i in range(len(sensorID)):
            sid = sensorID[i]
            cur.execute("""INSERT INTO sensor(ID, Type, Status) VALUES (%s, %s, %s)""", (sid, stype, status))
        mysql.connection.commit()
        cur.close()
        print("MySQL Data added!!!")


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/sensorDB"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootpass'
app.config['MYSQL_DB'] = 'sensorDB'

mysql = MySQL(app)

@app.route('/')
def my_option():
    return render_template("configure-options.html")


@app.route('/cluster_node')
def my_form():
    return render_template("node-form.html")


@app.route('/', methods=['POST'])
def my_form_post():
    if "my-form" in request.form:
        network = request.form['networkID']
        cluster = request.form['clusterID']
        latitude = request.form['lat']
        long = request.form['lon']
        my_cluster_node = ClusterNode(network, cluster, latitude, long)
        print(my_cluster_node.clusterID)
    elif "my-sensor-node-form" in request.form:
        cluster = request.form['clusterID']
        snode = request.form['sensorNodeID']
        latitude = request.form['lat']
        long = request.form['lon']
        my_sensor_node = SensorNode(cluster, snode, latitude, long)
        print(my_sensor_node.sensorNodeID)
    elif "my-sensor-form" in request.form:
        snodeID = request.form['sensorNodeID']
        type = request.form['sensorType']
        number = request.form['number']
        my_sensor = Sensor(snodeID, type, number)
        sensorIDlist = my_sensor.createSensorID(int(number))
        state = "on"
        sensorStatusList = my_sensor.set_sensor_status(sensorIDlist,state)
        #my_sensor.generate_mongo_sensor_data(sensorIDlist, type, state)
        my_sensor.generate_mysql_sensor_data(sensorIDlist, type, state)

    return render_template("configure-options.html")


@app.route('/sensor_node')
def my_sensor_node_form():
    return render_template("sensor-node-form.html")

'''
@app.route('/', methods=['POST'])
def my_sensor_node_form_post():
    cluster = request.form['ClusterID']
    snode = request.form['sensorNodeID']
    latitude = request.form['lat']
    long = request.form['lon']
    my_sensor_node = SensorNode(cluster, snode, latitude, long)
    print(my_sensor_node.snode)
    return render_template("configure-options.html")
'''

@app.route('/sensor')
def my_sensor_form():
    return render_template("sensor-form.html")

'''
@app.route('/', methods=['POST'])
def my_sensor_form_post():
    snodeID = request.form['sensorNodeID']
    type = request.form['sensorType']
    number = request.form['number']
    my_sensor = Sensor(snodeID, type, number)
    sensorIDlist = my_sensor.createSensorID(number)
    return render_template("configure-options.html")
'''


@app.route('/show_sensors')
def my_sensor_info_form():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sensor")
    data = cur.fetchall()
    return render_template("sensor_info.html", data=data)


if __name__ == '__main__':
    app.run()

