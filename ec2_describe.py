
import boto.ec2
import argparse
import os

def get_arg_parse():
        parser=argparse.ArgumentParser(description=_doc_, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('-r', '--region', choices=['us-west-2', 'eu-west-1', 'us-east-1', 'eu-central-1'], requi>
        return parser
class GetEC2Info(object):
        def _init_(self,args):
                try:
                        conn= boto.ec2.connect_to_region(self.region)
                        reservations= conn.get_all_reservations()
                        for res in reservations:
                                for inst in res.instances:
                                        if 'Name' in inst.tags:
                                                if 'Product' in inst.tags:
                                                        if 'Component' in inst.tags:
                                                                if 'Billing_Code' in inst.tags:
                                                                        if 'jira_ticket' in inst.tags:
                                                                                print (int.tags['Name'], inst.tags['>
                        if not('jira_ticket' in inst.tags):
                                if 'Name' in inst.tags:
                                        if 'Product'in inst.tags:
                                                print (inst.tags['Name'], inst.tags['Product'], inst.tags['Component>
                        if not ('Component' in inst.tags):
                                if 'Name' in inst.tags:
                                        if 'Product' in inst.tags:
                                                 print (inst.tags['Name'], inst.tags['Product'], inst.state, inst.in>
                        if not ('Product' in inst.tags):
                                if 'Name' in inst.tags:
                                        if 'Component' in inst.tags:
                                                print (inst.tags['Name'], inst.tags['Component'], inst.state, inst.i>
                        if not ('Name' in inst.tags):
                                 print (inst.state, inst.instance_type, inst.private_ip_address, inst.placement, ins>
                except boto.exception.EC2ResponseError as detail:
                        print ('EC2 error:', detail)
                        raise detail
parser= get_arg_parse()
args= parser.parse_args()
info= GetEC2Info(args)
info.list_ec2()

