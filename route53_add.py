
import boto.route53
import boto.ec2
import boto.utils
region_info={ 'us-west-2': { 'domains':['usw2.basecloud.io'],},
              'us-east-1': {'domains':['use1.basecloud.io'],},
              'us-east-2': {'domains':['use2.basecloud.io'],},
              'eu-west-1': {'domains':['euw1.basecloud.io'],},
              'eu-central':{'domains':['euc1.basecloud.io'],},
}

try:
        data=boto.utils.get_instance_identity()
        region=data['document']['region']
        ip_addr=data['document']['privateIp']
        instance_id=data['document']['instanceId']

        domains= region_info[region]['domains']
        ec2conn=boto.ec2.connect_to_region(region)
        reservations=ec2conn.get_all_instances(instance_ids=[instance_id])
        instance=reservations[0].instances[0]
        conn=boto.route53.connect_to_region(region)
        for domain in domains:
                zone=conn.get_zone(domain)
                fqdn=instance.tags['Name']+'.'+domain
                change_set=boto3.route53.record.ResourceRecordSets( conn, zone.id)
                changes1=change_set.add_change( "UPSERT", fqdn, type="A")
                changes1.add_value(ip_addr)
                change_set.commit()
                print( "Added an A record pointing %s to %s" % (fqdn, ip_addr))
except boto.route53.exception.DNSServerError as detail:
        print ('Route53 error:', detail)
        raise detail

