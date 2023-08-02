@echo off

rem Set the AWS access key ID
for /f "usebackq tokens=*" %%i in (`aws configure get aws_access_key_id`) do set AWS_ACCESS_KEY_ID=%%i

rem Check if the AWS_ACCESS_KEY_ID environment variable is set
if not defined AWS_ACCESS_KEY_ID (
    echo AWS_ACCESS_KEY_ID environment variable is not set
    exit /b 1
)

rem Set the AWS secret access key
for /f "usebackq tokens=*" %%i in (`aws configure get aws_secret_access_key`) do set AWS_SECRET_ACCESS_KEY=%%i

rem Check if the AWS_SECRET_ACCESS_KEY environment variable is set
if not defined AWS_SECRET_ACCESS_KEY (
    echo AWS_SECRET_ACCESS_KEY environment variable is not set
    exit /b 1
)


