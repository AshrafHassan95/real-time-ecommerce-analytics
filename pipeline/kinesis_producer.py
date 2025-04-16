import boto3
import json
import time
from data_generation.ai_data_generator import generate_data
from dotenv import load_dotenv
import os

load_dotenv()

class KinesisProducer:
    def __init__(self, stream_name):
        self.client = boto3.client(
            'kinesis',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.stream_name = stream_name
        
    def put_record(self, data, partition_key):
        response = self.client.put_record(
            StreamName=self.stream_name,
            Data=json.dumps(data),
            PartitionKey=partition_key
        )
        return response
        
    def generate_and_send_data(self):
        product_gen = ProductDataGenerator()
        user_gen = UserBehaviorGenerator()
        
        while True:
            # Generate and send product data
            product = product_gen.generate_product()
            self.put_record({
                'type': 'product',
                'data': product
            }, product['product_id'])
            
            # Generate and send user behavior
            for _ in range(random.randint(1, 5)):
                behavior = user_gen.generate_user_behavior()
                behavior['product_id'] = product['product_id']
                self.put_record({
                    'type': 'user_behavior',
                    'data': behavior
                }, behavior['user_id'])
                
            time.sleep(random.uniform(0.5, 2))

if __name__ == "__main__":
    producer = KinesisProducer('ecommerce-stream')
    producer.generate_and_send_data()
