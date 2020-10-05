#!/usr/bin/python3

import json
import paho.mqtt.client as mqtt
import time
import csv
import socket
import subprocess 
import zerorpc
import sys
import os

#read and close username and pass
userObj = open('/root/SAAM-lgtc/user','r')
user = userObj.readline().strip()
userObj.close
passwordObj = open('/root/SAAM-lgtc/pass','r')
password = passwordObj.readline().strip()
passwordObj.close 

#start mqtt client
client = mqtt.Client()
client.username_pw_set(user, password)
client.tls_set(ca_certs="/opt/cert/ca_certificate.pem",
                certfile="/opt/cert/client_certificate.pem",
                keyfile="/opt/cert/client_key.pem")
client.tls_insecure_set(True)
client.connect("mqtt.saam-platform.eu", 8883)

#read and close loc id
loc_id_Obj = open('/etc/lgtc/loc-id','r')
loc_id = loc_id_Obj.readline().strip()
loc_id_Obj.close

mqtt_topic = "saam/health/" + loc_id

status = {
            "timestamp": "1234566",
            "saam-pmc": "unknown",
            "saam-amb": "unknown"  
            }

def get_status(service_name):
	cntr = 1
	while True:
		avahi = subprocess.check_output(["avahi-browse","-rptk","_remote._tcp"])
		avahi = csv.reader(avahi.decode().split('\n'), delimiter=';')
		for row in avahi:
			if row and row[0] == "=" and service_name in row:
				try:
					status = "up"
					return status
				except socket.error:
					pass
		time.sleep(5)
		cntr += 1
		if cntr > 3:
			status = "down"
			return status



		
			
#first start avahi-daemon with "service_name"
status["timestamp"] = int(round(time.time()*1000))
status["saam-pmc"] = get_status("saam-pmc")
status["saam-amb"] = get_status("saam-amb")
status["saam-gw"] = "up"

print(mqtt_topic)
print(json.dumps(status))
client.publish(topic=mqtt_topic, payload=json.dumps(status))


    
   
    








