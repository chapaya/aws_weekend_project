import boto3
import sys
from pprint import pprint

#ec2ir = boto3.client('ec2', region_name='us-east-1')
ec2client = boto3.client('ec2', region_name='us-east-1')
ec2resource = boto3.resource('ec2', region_name='us-east-1')

def get_name(fid):
    """
    Find server name according to server id
    :param fid: server id
    :return:instancename
    """
    ec2instance = ec2resource.Instance(fid)
    instancename = ''
    for tags in ec2instance.tags:
        #print(tags) # print all tags
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    return(instancename)

def get_weekend_tag_value(fid):
    """
    Find tag value of instance tag Weekend
    :param fid: server id
    :return: Weekend tag value
    """
    ec2instance = ec2resource.Instance(fid)
    instancename = ''
    for tags in ec2instance.tags:
        #print(tags) # print all tags
        if tags["Key"] == 'Weekend':
            tag_value = tags["Value"]
    return tag_value

# Main program #
def main():
    instances = ec2client.describe_instances(Filters=[{'Name': 'tag:Weekend', 'Values': ['True'] }]) # instances that has tag Weekend with any value
    print(instances)
    print(instances['Reservations'])
    if instances['Reservations'] == []:
        print("No ec2 server has tag Weekend=True .. bye..")
        sys.exit()

    ids = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(instance["InstanceId"])
            ids.append(instance['InstanceId'])

    print(ids)
    #Start instances
    ec2client.start_instances(InstanceIds=ids)
    print('Started your instances: ' + str(ids))

    response = ec2client.describe_instance_status(
         InstanceIds=[
            'i-0a5448168783adce5',
         ],
     )

    pprint(response)

    # for instance in ids:
    #     print("Instance status of " + instance.id + instance.state)
    # ec2 = boto3.resource('ec2')
    for instance in ec2resource.instances.all():
        print(instance.id, instance.state)


if __name__ == "__main__":
    main()

