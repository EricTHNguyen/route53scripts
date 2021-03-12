import os
import sys
import time
import requests
import boto.vpc
from boto.vpc import VPCConnection

insideFTDv1 = 'PRIVATE_IP_PING'
insideFTDv2 = 'PRIVATE_IP_PING'
eniFTDv1 = 'ENI_OF_FTD1'
eniFTDv2 = 'ENI_OF_FTD2'
routeTable = 'ROUTING_TABLE'
vpc = boto.vpc.connect_to_region('us-west-2')
rtb = vpc.get_all_route_tables(route_table_ids=routeTable)
apiURL = 'API_CALL_TO_REPORT_STATUS'
headers = {'content-type': "application/json", 'cache-control': "no-cache"}

def routePdFTDV1():
    vpc.replace_route(route_table_id=routeTable,
                      destination_cidr_block='0.0.0.0/0',
                      interface_id=eniFTDv1)
    vpc.replace_route(route_table_id=routeTable,
                      destination_cidr_block='10.10.0.0/24',
                      interface_id=eniFTDv1)
    vpc.replace_route(route_table_id=routeTable,
                      destination_cidr_block='10.11.0.0/24',
                      interface_id=eniFTDv1)

def routePdFTDV2():
    vpc.replace_route(route_table_id=routeTable,
                      destination_cidr_block='0.0.0.0/0',
                      interface_id=eniFTDv2)
    vpc.replace_route(route_table_id=routeTable,
                      destination_cidr_block='10.20.0.0/24',
                      interface_id=eniFTDv2)
    vpc.replace_route(route_table_id=routeTable,
                      destination_cidr_block='10.21.0.0/24',
                      interface_id=eniFTDv2)

for rt in rtb:
    for a in rt.routes:
        eniRTB = a.interface_id

valid = True
while valid:
        insidePing1 = os.system("ping -c 15 -w 5 "+insideFTDv1+"|grep -c '100% packet loss'")
        insidePing1 = os.system("ping -c 15 -w 5 "+insideFTDv2+"|grep -c '100% packet loss'")
  # insidePing1 IP exit with 0 failure
    # Lock file doesn't exsist
if insidePing1==0 and (not os.path.isfile('/tmp/ftdv_lock')):
  # if eniRTB not equal to ENI2 then change route
        if eniRTB==eniFTDv1:
                routePDFTDV2()
                payload='{"HostName": "Status":"0", "comments": "FAILURE FTDv1: Changing to FTDv2 route, ENI="}'
                response= requests.post(apiURL, data=payload, headers=headers)

                with open('/var/log/ftdv.log', 'a') as f:
                        sys.stdout=f
                        print(time.strftime("%c"),":","FAILURE us-west-2: Changing to FTDv2 route, ENI=", eniFTDv2, >
 # insidePing2 IP exit with 0 failure
                # insidePing1 exit with 256 code
                        if insidePing2==0 and insidePing1==256:
                                if eniRTB==eniFTDv2:
                                        routPdFTDV1()
                                        os.system('/bin/touch /tmp/ftdv_lock')
                                        payload=' { "HostName", "Status":"0", "comments":"FAILURE FTDv2: Changing to>
                                        response = requests.post(apiURL, data=payload, headers=headers)

                                        with open('/var/log/ftdv.log', 'a') as f:
                                                sys.stdout=f
                                                print (time.strftime("%c"), ":", "FAILURE eu-west-1: Changing tp FTD>
elif eniRTB == eniFTdv2:
        payload='{ "HostName":"", "status":"1", "Comments": "insideFTDv2 => up &using"}'
        respose=requests.post(apiURL, data=payload, headers=headers)
        with open('/var/log/ftdv.log', 'a') as f:
                sys.stdout=f
                print(time.strftime("%c"),": insideFTDv2 => is up & ENI =>", eniFTDv2, response.text, insidePing1, i>

