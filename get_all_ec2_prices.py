import boto3
import json

# Set up the Boto3 client for Pricing API
pricing_client = boto3.client('pricing', region_name='us-east-1')  # Replace with your desired region

# Describe EC2 services to get service code for EC2 instances
ec2_services = pricing_client.describe_services(ServiceCode='AmazonEC2')
ec2_service_code = ec2_services['Services'][0]['ServiceCode']

print (f"ec2_service_code:{ec2_service_code}")

# Fetch available EC2 instance types in the region
instance_types = pricing_client.get_attribute_values(
    ServiceCode=ec2_service_code,
    AttributeName='instanceType')['AttributeValues']

# Fetch prices for each instance type
prices = {}
for instance_type in instance_types:
    response = pricing_client.get_products(
        ServiceCode=ec2_service_code,
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type['Value']},
            # You can add more filters like OS, tenancy, etc. here
        ]
    )

    #print (f"instance_type:{instance_type}")
    str = response['PriceList'][0]
    str1 = json.loads(str)
    #test2 = test1['terms']['OnDemand']['24T8BV232565G39C.JRTCKXETXF']['priceDimensions']['24T8BV232565G39C.JRTCKXETXF.6YS6EN2CT7']['pricePerUnit']['USD']
    instance_kind = next(iter(str1['terms']))
    if 'OnDemand' not in instance_kind:
        continue
    str2= str1['terms']['OnDemand']
    str3 = next(iter(str2))
    str4 = str2[str3]['priceDimensions']
    #print (f"str4:{str4}")
    str5 = next(iter(str4))
    #print (f"str5:{str5}")
    str6 = str4[str5]['pricePerUnit']
    #print (f"str6:{str6}")
    instance_currency = next(iter(str6))
    if instance_currency == 'USD':
        instance_price = str6[instance_currency] 
    else :
        continue

    # Print or store the pricing information
    print(f"Instance Type: {instance_type['Value']}  Price Per Unit[USD]: {instance_price}")
