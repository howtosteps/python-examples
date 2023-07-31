import boto3

def get_ec2_pricing(instance_type, region='us-east-1'):
    pricing_client = boto3.client('pricing', region_name=region)

    response = pricing_client.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'instanceType',
                'Value': instance_type,
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': region,
            },
        ],
    )

    price_list = response['PriceList']
    if price_list:
        return float(price_list[0]['terms']['OnDemand']['USD'])
    else:
        return None

def get_all_ec2_instances_with_pricing():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances()

    instances_list = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_info = {
                'InstanceId': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],
                'PublicIP': instance.get('PublicIpAddress', 'N/A'),
                'PrivateIP': instance.get('PrivateIpAddress', 'N/A'),
                'AvailabilityZone': instance['Placement']['AvailabilityZone'],
            }

            instance_type = instance['InstanceType']
            instance_info['PricePerHour'] = get_ec2_pricing(instance_type)
            instance_info['TotalCostPerHour'] = instance_info['PricePerHour'] if instance_info['PricePerHour'] else 'N/A'

            instances_list.append(instance_info)

    return instances_list

if __name__ == "__main__":
    ec2_instances = get_all_ec2_instances_with_pricing()
    for instance in ec2_instances:
        print(instance)
