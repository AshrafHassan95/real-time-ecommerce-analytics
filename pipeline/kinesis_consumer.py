import boto3
import json
import pymysql
from dotenv import load_dotenv
import os
from datetime import datetime
import time

load_dotenv()

kinesis = boto3.client(
    'kinesis',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def process_record(record):
    data = json.loads(record['Data'].decode('utf-8'))
    
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    
    try:
        with connection.cursor() as cursor:
            # Store the activity
            cursor.execute("""
                INSERT INTO user_activity (user_id, product_id, activity_type, activity_data)
                VALUES (%s, %s, %s, %s)
            """, (data['user_id'], data['product_id'], data['activity_type'], json.dumps(data)))
            
            # Update product popularity metrics (simplified example)
            if data['activity_type'] == 'purchase':
                cursor.execute("""
                    UPDATE products 
                    SET stock = stock - 1 
                    WHERE product_id = %s
                """, (data['product_id'],))
            
            connection.commit()
            print(f"Processed {data['activity_type']} for product {data['product_id']}")
    finally:
        connection.close()

def consume_stream():
    shard_iterator = kinesis.get_shard_iterator(
        StreamName=os.getenv('KINESIS_STREAM_NAME'),
        ShardId='shardId-000000000000',  # Single shard in our setup
        ShardIteratorType='LATEST'
    )['ShardIterator']
    
    while True:
        response = kinesis.get_records(
            ShardIterator=shard_iterator,
            Limit=100
        )
        
        for record in response['Records']:
            process_record(record)
        
        shard_iterator = response['NextShardIterator']
        time.sleep(1)  # Poll every second

if __name__ == "__main__":
    consume_stream()