#!/bin/bash

# Load environment variables
source ../.env

# Create Kinesis stream
aws kinesis create-stream \
  --stream-name $KINESIS_STREAM_NAME \
  --shard-count 1 \
  --region $AWS_REGION

echo "Kinesis stream '$KINESIS_STREAM_NAME' created in region '$AWS_REGION'"
