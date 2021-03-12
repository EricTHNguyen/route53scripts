import time
import sys
import subprocess
import boto.route53
import argparse

Conn=boto.route53.connect_to_region('us-west-2')
def get_arg_parse():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--region', choices=['us-west-2', 'eu-west-1', 'us-east-1', 'eu-central-1'], required = False, default='us-west-2',
                        help="Region to connect to")
    return parser
parser = get_arg_parse()
args = parser.parse_args()
valid =True
while valid:
        Route53URLip = 'prod-stack001.basecloud.io'
        URLcurr = 'prod-stack-002.basecloud.io'
        Route53Domain = 'basecloud.io'
        CheckRoute53DNS = subprocess.check_output(['dig', '+tcp', '+short', Route53URLip])
        CheckSQLDNS = subprocess.check_output(['dig','+tcp', '+short', URLcurr])
        if CheckSQLDNS != "":
                if CheckSQLDNS != CheckRoute53DNS:
                        Zone = Conn.get_zone( Route53Domain )
                        ChangeSet = boto.route53.record.ResourceRecordSets(Conn, Zone.id)
                        Changes1 = ChangeSet.add_change("UPSERT", Route53URLip, type="A")
                        Changes1.add_value(CheckSQLDNS)
                        ChangeSet.commit()
                        with open('/var/log/check_ip.log', 'a') as f:
                                sys.stdout = f
                                print (time.strftime("%c"), "DNS changed to ... ", CheckSQLDNS,)
                else:
                 with open('/var/log/check_ip.log', 'a') as f:
                        sys.stdout = f
                        print (time.strftime("%c"), "DNS is still ... Route53 =>", CheckRoute53DNS,)
        else:
                 with open('/var/log/check_ip.log', 'a') as f:
                        sys.stdout = f
                        print (time.strftime("%c"), "Endpoint returns empty string, please check DNS", URLcurr,time.sleep(10))
                        # testing
