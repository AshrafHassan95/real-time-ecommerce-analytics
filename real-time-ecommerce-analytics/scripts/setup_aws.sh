#!/bin/bash

# This script sets up AWS resources needed for the project

# Configure AWS CLI
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set default.region $AWS_REGION

# Create Kinesis stream
aws kinesis create-stream --stream-name ecommerce-stream --shard-count 1

# Create Lambda function
aws lambda create-function \
    --function-name process-ecommerce-stream \
    --runtime python3.8 \
    --handler process_stream.lambda_handler \
    --role $LAMBDA_ROLE_ARN \
    --zip-file fileb://lambda_functions/process_stream.py \
    --environment Variables={DB_HOST=$DB_HOST,DB_USER=$DB_USER,DB_PASSWORD=$DB_PASSWORD}

# Connect Kinesis to Lambda
aws lambda create-event-source-mapping \
    --event-source-arn arn:aws:kinesis:$AWS_REGION:$AWS_ACCOUNT_ID:stream/ecommerce-stream \
    --function-name process-ecommerce-stream \
    --starting-position LATEST

echo "AWS resources setup complete"
