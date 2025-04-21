import json
import random
import time
import pymysql
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
import boto3

load_dotenv()

# Initialize AWS session
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
kinesis = session.client('kinesis')

def get_random_user_and_product():
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    
    try:
        with connection.cursor() as cursor:
            # Get random user
            cursor.execute("SELECT user_id FROM users ORDER BY RAND() LIMIT 1")
            user_result = cursor.fetchone()
            if not user_result:
                raise ValueError("No users found in database")
            user_id = user_result[0]
            
            # Get random product
            cursor.execute("SELECT product_id FROM products ORDER BY RAND() LIMIT 1")
            product_result = cursor.fetchone()
            if not product_result:
                raise ValueError("No products found in database")
            product_id = product_result[0]
            
            return user_id, product_id
    finally:
        connection.close()

def generate_user_activity():
    activities = ['view', 'add_to_cart', 'purchase']
    
    while True:
        try:
            user_id, product_id = get_random_user_and_product()
            activity_type = random.choices(
                activities,
                weights=[0.7, 0.2, 0.1]  # 70% view, 20% add to cart, 10% purchase
            )[0]
            
            activity_data = {
                "user_id": user_id,
                "product_id": product_id,
                "activity_type": activity_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": f"session_{random.randint(1000, 9999)}",
                "device": random.choice(['mobile', 'desktop', 'tablet'])
            }
            
            # Send to Kinesis
            response = kinesis.put_record(
                StreamName=os.getenv('KINESIS_STREAM_NAME'),
                Data=json.dumps(activity_data),
                PartitionKey=str(product_id)
            )
            
            print(f"Sent activity: {activity_type} for product {product_id} by user {user_id}")
            print(f"Kinesis response: {response}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(random.uniform(0.5, 2))  # Simulate real-time events

if __name__ == "__main__":
    generate_user_activity()