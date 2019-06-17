#https://stackoverflow.com/questions/46379043/boto3-wait-until-running-doesnt-work-as-desired
import boto3
from pprint import pprint


ec2 = boto3.resource('ec2')
ec2client = boto3.client('ec2')

# with ec2 resource
instance = ec2.Instance('i-0a5448168783adce5')
print(instance.state)
print(instance.state['Name'])  # instance status
print(instance.launch_time)
print(instance.image_id)
instance.wait_until_running()
print(instance.state)


for instance in ec2.instances.all():
    print(instance.id, instance.state)

# with ec2 client
response = ec2client.describe_instance_status(
         InstanceIds=[
            'i-0a5448168783adce5',
         ],
     )

pprint(response)


'''
{'Code': 16, 'Name': 'running'}
running
2019-06-17 17:04:16+00:00
ami-024a64a6685d05041
{'Code': 16, 'Name': 'running'}
i-0a5448168783adce5 {'Code': 16, 'Name': 'running'}
'''