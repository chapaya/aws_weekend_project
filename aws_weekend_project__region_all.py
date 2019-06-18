import boto3
import sys
from pprint import pprint

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
    #script_action = sys.argv[1]  # Can be start or stop
    script_action = 'start' #sys.argv[1]  # Can be start or stop
    regions = ['us-east-1', 'eu-west-1']
    for region in regions:
        print('Checking region: ' + region)
        ec2client = boto3.client('ec2', region_name=region)
        ec2resource = boto3.resource('ec2', region_name=region)
        instances = ec2client.describe_instances(Filters=[{'Name': 'tag:Weekend', 'Values': ['True'] }]) # instances that has tag Weekend with any value
        #print(instances)
        #print(instances['Reservations'])
        if instances['Reservations'] == []:
            print("No ec2 server has tag Weekend=True .. bye..")
            continue # exit from loop

        ids = []

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                #print(instance["InstanceId"])
                ids.append(instance['InstanceId'])

        print(ids)
        print('Servers status before... ')
        for id in ids:
            server = ec2resource.Instance(id)
            print('server ' + id + ' - ' + get_name(id) + ' status: ' + server.state['Name'])

        #Doing the action that was choosen
        if script_action == 'start':
            print('Starting servers ... ')
            for id in ids:
                server = ec2resource.Instance(id)
                print('Working on server ' + id + ' - ' + get_name(id) + ' status: ' + server.state['Name'])
                server.start()
                server.wait_until_running()
                print('server ' + id + ' - ' + get_name(id) + ' status: ' + server.state['Name'])
        elif script_action == 'stop':
            for id in ids:
                server = ec2resource.Instance(id)
                print('Working on server ' + id + ' - ' + get_name(id) + ' status: ' + server.state['Name'])
                server.stop()
                server.wait_until_stopped()
                print('server ' + id + ' - ' + get_name(id) + ' status: ' + server.state['Name'])
        else:
            print('Script action must be start or stop ! .. bye')
            sys.exit()

        print('Servers status after ... ')
        for id in ids:
            server = ec2resource.Instance(id)
            print('server ' + id + ' - ' + get_name(id) + ' status: ' + server.state['Name'])

        print('program ended!')


if __name__ == "__main__":
    main()

