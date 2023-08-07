import boto3
import json

def get_ec2_instance_hourly_price(region_code, 
                                  instance_type, 
                                  preinstalled_software='NA', 
                                  tenancy='Shared', 
                                  is_byol=False):
                                       
    if is_byol:
        license_model = 'Bring your own license'
    else:
        license_model = 'No License required'

    if tenancy == 'Host':
        capacity_status = 'AllocatedHost'
    else:
        capacity_status = 'Used'
    
    filters = [
        {'Type': 'TERM_MATCH', 'Field': 'termType', 'Value': 'OnDemand'},
        {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': capacity_status},
        {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region_code},
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
        {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': tenancy},
        {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': preinstalled_software},
        {'Type': 'TERM_MATCH', 'Field': 'licenseModel', 'Value': license_model},
    ]

    pricing_client = boto3.client('pricing', region_name='us-east-1')
    
    response = pricing_client.get_products(ServiceCode='AmazonEC2', Filters=filters)

    print (f"response:{response}")
    for price in response['PriceList']:
        price = json.loads(price)

        print(price['terms']['OnDemand'].values()) 
        for on_demand in price['terms']['OnDemand'].values():
            for price_dimensions in on_demand['priceDimensions'].values():
                price_value = price_dimensions['pricePerUnit']['USD']
            
        return float(price_value)
    
    return None



def get_all_ec2_instances_with_pricing(region='us-east-1'):
    ec2_client = boto3.client('ec2',region_name=region)
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
            
            ec2_instance_price = get_ec2_instance_hourly_price(
                region_code=region, 
                instance_type=instance_type, 
            )   
            
            instance_info['PricePerHour'] = ec2_instance_price
            instance_info['TotalCostPerHour'] = instance_info['PricePerHour'] if instance_info['PricePerHour'] else 'N/A'
            instances_list.append(instance_info)

    return instances_list


if __name__ == "__main__":
    print("Function 1 :Getting EC2 instances with pricing")
    ec2_instances = get_all_ec2_instances_with_pricing()
    for instance in ec2_instances:
        print(instance)

