# EC2 Examples

## Managing EC2 Instances with Boto3

### 1. Launching an EC2 Instance
```python
import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')

instances = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0',  # Example Amazon Linux AMI
    MinCount=1,
    MaxCount=1,
    InstanceType='t3.micro',
    KeyName='my-key-pair',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'DevInstance'},
                {'Key': 'Project', 'Value': 'DeepAgents'}
            ]
        }
    ]
)
print("Launched Instance ID:", instances[0].id)
```

### 2. Listing Running Instances
```python
import boto3

ec2_client = boto3.client('ec2')

response = ec2_client.describe_instances(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
)

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(f"ID: {instance['InstanceId']} | Type: {instance['InstanceType']} | State: {instance['State']['Name']}")
```

### 3. Stopping and Terminating an Instance
```python
import boto3

ec2_client = boto3.client('ec2')

# Stop instance
ec2_client.stop_instances(InstanceIds=['i-0123456789abcdef0'])

# Terminate instance
ec2_client.terminate_instances(InstanceIds=['i-0123456789abcdef0'])
```
