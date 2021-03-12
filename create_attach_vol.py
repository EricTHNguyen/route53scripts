
import boto.ec2
import os
import sys
import time
import boto.utils
import subprocess

data = boto.utils.get_instance_identity()
region = data['document']['region']
instance_id = data['document']['instanceId']
availabilityZone = data['document']['availabilityZone']

# Check Volume exsist or not
aws_r = boto.ec2.connect_to_region(region)
reservations = aws_r.get_all_instances(instance_ids=[instance_id])
instance = reservations[0].instances[0]
volName = instance.tags['Name'] + '_xvdg'
volExsist = "aws ec2 describe-volumes --region %s --filters Name=tag-key,Values='Name' Name=tag-value,Values=%s --qu>
volume =  subprocess.check_output(volExsist, shell=True)

sysDeviceID = '/dev/xvdg'
sysDeviceMount = '/mnt/es/elasticsearch'
sysFileType = 'ext4'
addFStabCMD = "echo '/dev/xvdg /mnt/es/elasticsearch ext4 defaults 0 0' >> /etc/fstab"
grabHostname = instance.tags['Name']
addHostname = "echo %s > /tmp/es_hostname.txt" %grabHostname
es_hostname =  subprocess.check_output(addHostname, shell=True)

def CreateVolume():
    aws_r = boto.ec2.connect_to_region(region)
    vol = aws_r.create_volume(3000, availabilityZone, volume_type='io1', iops='5000', encrypted=True)
    chk_vol = aws_r.get_all_volumes([vol.id])[0]
    reservations = aws_r.get_all_instances(instance_ids=[instance_id])
    instance = reservations[0].instances[0]
    volName = instance.tags['Name'] + '_xvdg'
    aws_r.create_tags([vol.id], {"Name":volName})

    print ('Instance Id:', instance_id)
    print ('Volume Id:', vol.id)
    print ('Volume Status:', chk_vol.status)
    print ('Volume Zone:', chk_vol.zone)
    print ('Volume Device:', chk_vol.attach_data.device)

    for _ in range(0,15):
        avail = 'available'
        aws_r = boto.ec2.connect_to_region(region)
        chk_vol = aws_r.get_all_volumes([vol.id])[0]
        print ('Waiting for Volume', chk_vol.status)
        if chk_vol.status  == avail:
            attach  = aws_r.attach_volume(vol.id, instance_id, sysDeviceID)
            print ('Attach Volume Result: ', attach)
            break
        aws_r.close()
        time.sleep(1)
    time.sleep(5)
    mkfs = subprocess.check_output(['mkfs.ext4', sysDeviceID])
    addDir = subprocess.check_output(['mkdir', '-p', sysDeviceMount])
    addFSTAB = subprocess.check_output(addFStabCMD, shell=True)
    Mount = subprocess.check_output(['mount', sysDeviceID, sysDeviceMount])

def AttachExsistingVolume():
    for _ in range(0,15):
        avail = 'available'
        aws_r = boto.ec2.connect_to_region(region)
        chk_vol = aws_r.get_all_volumes(volume)[0]

        print ('Waiting for Attaching Volume', chk_vol.status)
        if chk_vol.status  == avail:
            attach  = aws_r.attach_volume(volume, instance_id, sysDeviceID)
            print ('Attach Volume Result: ', attach)
            break
        aws_r.close()
        time.sleep(1)
    time.sleep(5)
    addDir = subprocess.check_output(['mkdir', '-p',  sysDeviceMount])
    addFSTAB = subprocess.check_output(addFStabCMD, shell=True)
    Mount = subprocess.check_output(['mount', sysDeviceID, sysDeviceMount])

if volume == '':
    print (volume)
    CreateVolume()
else:
    print (volume)
    AttachExsistingVolume()

