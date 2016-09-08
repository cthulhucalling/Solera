#!/usr/bin/python

from SoleraConnector import SoleraConnector
from datetime import datetime
from Solerafunctions import query_for_artifacts,get_artifact_details,export_artifact
import json
import time

gmtoffset="-06:00"
default_date=datetime.now()
start_date=raw_input("Enter start date ["+default_date.strftime('%Y-%m-%d')+"]: ")
if not start_date:
        start_date=default_date.strftime('%Y-%m-%d')
start_time=raw_input("Enter start time ["+default_date.strftime('%H:%M:%S')+"]: ")
if not start_time:
        start_time=default_date.strftime('%H:%M:%S')
end_date=raw_input("Enter end date ["+default_date.strftime('%Y-%m-%d')+"]: ")
if not end_date:
        end_date=default_date.strftime('%Y-%m-%d')
end_time=raw_input("Enter end time ["+default_date.strftime('%H:%M:%S')+"]: ")
if not end_time:
        end_time=default_date.strftime('%H:%M:%S')
ip_addr=raw_input("Enter IP address: ")

#print start_date
#print start_time
#print end_date
#print end_time

percent_complete=0
while percent_complete < 100:
        z=query_for_artifacts(start_date,start_time,end_date,end_time,gmtoffset,ip_addr)
        print "Query is "+z['result']['percentcomplete']+"% complete"
        percent_complete=int(z['result']['percentcomplete'])
        time.sleep(10)

print z["result"]["search_status"]
print "Number of results: %s" %z["result"]["numResults"]

for artifact in z['result']['sorted_artifacts']:
        print "%s %s" %(artifact['Artifact']['id'],artifact['Artifact']['title'])

while True:
        print "\r\n"
        action_select=raw_input("export artifact or detail: ")
        if action_select=="exit":
                import sys
                sys.exit()
        elif action_select=="detail":
                selected_artifact=raw_input("Artifact ID: ")
                get_artifact_details(selected_artifact)
        elif action_select=="export":
                selected_artifact=raw_input("Artifact ID: ")
                export_artifact(selected_artifact)



