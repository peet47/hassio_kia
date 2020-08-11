#!/usr/bin/python

#################
#
#
# get the KIa stuff....
#
#   Peter Massini
#
#	Python 3.7
#
#
#################

import sys, os
import requests
import json
from time import sleep
import paho.mqtt.client as mqtt

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

#VAR
mqtt_host = "<IP>"
mqtt_port = 1883
mqtt_username = "<USER>"
mqtt_password = "<PASSWORD>"

cookies = {
    'ASP.NET_SessionId': '<SESSIONID>',
    'NL_MyKiaLogin': '_LoginGuid=<EMAIL>',
}

headers = {
    'Content-Length': '0',
    'authority': 'www.kia.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla / 5.0 (Linux; Android 7.0; SM-G892A Build / NRD90M; wv) AppleWebKit / 537.36 (KHTML, like Gecko) Version / 4.0 Chrome / 60.0.3112.107 Mobile Safari / 537.36 gonative',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
}

url = "https://www.kia.com/nl/webservices/mykia/connectedcar.asmx/GetCanbusData"

class car():
    def __init__(self):
        return

    def call(self):
        conn = requests.post(url=url, headers=headers, cookies=cookies)
        if conn.status_code == 403:
            print("Unauthenticated")
            sys.exit()
        if conn.status_code == 502:
            print("502: Server Error")
            sys.exit()
        #print(conn)
        self.json = conn.json()
        conn.close()
        return self

def send_stuff(mashina):
    #open the connection
    client = mqtt.Client(client_id="CAR", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
    client.username_pw_set(username=mqtt_username, password=mqtt_password)
    client.connect_async(host=mqtt_host, port=mqtt_port)
    client.loop_start()
    client.publish("mashina/car/ModelCode",payload=str(mashina.ModelCode), qos=1)
    client.publish("mashina/car/Model",payload=str(mashina.Model), qos=1)
    client.publish("mashina/car/PathToModelImage",payload=str(mashina.PathToModelImage), qos=1)
    client.publish("mashina/status/fuelLevel",payload=str(mashina.fuelLevel), qos=1)
    client.publish("mashina/status/fuelStatus",payload=str(mashina.fuelStatus), qos=1)
    client.publish("mashina/status/DoorsLocked",payload=str(mashina.DoorsLocked), qos=1)
    client.publish("mashina/status/Handbrake",payload=str(mashina.Handbrake), qos=1)
    client.publish("mashina/status/Range",payload=str(mashina.Range), qos=1)
    client.publish("mashina/status/odoMeter",payload=str(mashina.odoMeter), qos=1)
    client.publish("mashina/status/Tire/Pressure/FrontLeft",payload=str(mashina.TirePressureFrontLeft), qos=1)
    client.publish("mashina/status/Tire/Pressure/FrontRight",payload=str(mashina.TirePressureFrontRight), qos=1)
    client.publish("mashina/status/Tire/Pressure/RearLeft",payload=str(mashina.TirePressureRearLeft), qos=1)
    client.publish("mashina/status/Tire/PressureRearRight",payload=str(mashina.TirePressureRearRight), qos=1)
    client.publish("mashina/status/Tire/Warning",payload=str(mashina.TireWarning), qos=1)
    client.publish("mashina/status/Tire/Status/FrontLeft",payload=str(mashina.TireStatusFrontLeft), qos=1)
    client.publish("mashina/status/Tire/Status/FrontRight",payload=str(mashina.TireStatusFrontRight), qos=1)
    client.publish("mashina/status/Tire/Status/RearLeft",payload=str(mashina.TireStatusRearLeft), qos=1)
    client.publish("mashina/status/Tire/Status/RearRight",payload=str(mashina.TireStatusRearRight), qos=1)
    client.publish("mashina/status/Geo/Lattitude",payload=str(mashina.Lattitude), qos=1)
    client.publish("mashina/status/Geo/Longitude",payload=str(mashina.Longitude), qos=1)
    location_json = {"longitude": mashina.Longitude, "latitude": mashina.Lattitude}
    client.publish("mashina/status/Geo/location",payload=json.dumps(location_json), qos=1)
    client.publish("mashina/status/ev/soc",payload=str(mashina.evsoc), qos=1)
    client.publish("mashina/status/ev/charging",payload=str(mashina.evcharging), qos=1)
    client.publish("mashina/status/ev/isPlugged",payload=str(mashina.evisPlugged), qos=1)
    client.publish("mashina/status/ev/timeUntillCharged",payload=str(mashina.evtimeUntillCharged), qos=1)
    client.publish("mashina/status/drivingStyle/eco",payload=str(mashina.drivingStyleeco), qos=1)
    client.publish("mashina/status/drivingStyle/normal",payload=str(mashina.drivingStylenormal), qos=1)
    client.publish("mashina/status/drivingStyle/sport",payload=str(mashina.drivingStylesport), qos=1) 
    client.loop_stop()
    #we are done, lets close
    client.disconnect()

#create kia object
kia = car()
data = kia.call()
#car info
kia.ModelCode = data.json['SelectedCar']['ModelCode']
kia.Model = data.json['SelectedCar']['Model']
kia.PathToModelImage = "https://www.kia.com" + data.json['SelectedCar']['PathToModelImage']
#canbus info
kia.fuelLevel = data.json['CanbusLast']['fuelLevel']
kia.fuelStatus = data.json['CanbusLast']['fuelStatus']
kia.DoorsLocked = data.json['CanbusLast']['DoorsLocked']
kia.Handbrake = data.json['CanbusLast']['Handbrake']
kia.Range = data.json['CanbusLast']['Range']
kia.odoMeter = data.json['CanbusLast']['odoMeter']
kia.TirePressureFrontLeft = data.json['CanbusLast']['TirePressure']['FrontLeft']
kia.TirePressureFrontRight = data.json['CanbusLast']['TirePressure']['FrontRight']
kia.TirePressureRearLeft = data.json['CanbusLast']['TirePressure']['RearLeft']
kia.TirePressureRearRight = data.json['CanbusLast']['TirePressure']['RearRight']
kia.TireWarning = data.json['CanbusLast']['TireWarning']
kia.TireStatusFrontLeft = data.json['CanbusLast']['TireStatus']['FrontLeft']
kia.TireStatusFrontRight = data.json['CanbusLast']['TireStatus']['FrontRight']
kia.TireStatusRearLeft = data.json['CanbusLast']['TireStatus']['RearLeft']
kia.TireStatusRearRight = data.json['CanbusLast']['TireStatus']['RearRight']
kia.Lattitude = data.json['CanbusLast']['position']['Lattitude']
kia.Longitude = data.json['CanbusLast']['position']['Longitude']
kia.evsoc = data.json['CanbusLast']['ev']['soc']
kia.evcharging = data.json['CanbusLast']['ev']['charging']
kia.evisPlugged = data.json['CanbusLast']['ev']['isPlugged']
kia.evtimeUntillCharged = data.json['CanbusLast']['ev']['timeUntillCharged']
kia.evaverageUsage = data.json['CanbusLast']['ev']['averageUsage']
kia.drivingStyleeco = data.json['CanbusLast']['drivingStyle']['eco']
kia.drivingStylenormal = data.json['CanbusLast']['drivingStyle']['normal']
kia.drivingStylesport = data.json['CanbusLast']['drivingStyle']['sport']

send_stuff(kia)