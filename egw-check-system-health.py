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
 
client = mqtt.Client()
client.username_pw_set("DeviceUser", "b9BpukeK")
client.tls_set(ca_certs="/opt/cert/ca_certificate.pem",
                certfile="/opt/cert/client_certificate.pem",
                keyfile="/opt/cert/client_key.pem")
client.tls_insecure_set(True)
client.connect("mqtt.saam-platform.eu", 8883)

loc_id = open('/etc/lgtc/loc-id').readline().strip()
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


    
   
    








