import boto3
import sys
# Script start all instances that has tag Weekend=TRUE in IR and tag them with Expiration and RequestedBy
# By Eran Grimberg
# Script get 2 paramaters expiration_date and requested_by and tag the instances .
# start_kuku_servers.py $expiration_date $requested_by

#ec2ir = boto3.client('ec2', region_name='us-east-1')
ec2client = boto3.client('ec2', region_name='us-east-1')
ec2resource = boto3.resource('ec2', region_name='us-east-1')

def get_name(fid):
    ec2instance = ec2resource.Instance(fid)
    instancename = ''
    for tags in ec2instance.tags:
        #print(tags) # print all tags
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    return(instancename)

#instances = ec2.describe_instances(Filters=[{'Name': 'tag:Purpose', 'Values': ['KUKU']}]) # All instances that has tag Purpose=KUKU

instances = ec2client.describe_instances()
ids = []

for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        print(instance["InstanceId"])
        ids.append(instance['InstanceId'])

print(ids)

#Start instances
#ec2ir.start_instances(InstanceIds=ids)
print('Started your instances: ' + str(ids))


