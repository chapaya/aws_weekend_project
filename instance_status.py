
import boto3

ec2 = boto3.resource('ec2')
instance = ec2.Instance('i-0a5448168783adce5')
print(instance.state)
print(instance.launch_time)
print(instance.image_id)

for instance in ec2.instances.all():
    print(instance.id, instance.state)