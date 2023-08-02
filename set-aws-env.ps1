# Set the AWS access key ID
$Env:AWS_ACCESS_KEY_ID=aws configure get aws_access_key_id

# Set the AWS secret access key
$Env:AWS_SECRET_ACCESS_KEY=aws configure get aws_secret_access_key

# Set the AWS region
$Env:AWS_DEFAULT_REGION=aws configure get region
