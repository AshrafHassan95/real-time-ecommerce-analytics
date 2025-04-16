import boto3
import json
from database.queries import DatabaseQueries
from dotenv import load_dotenv
import os

load_dotenv()

class KinesisConsumer:
    def __init__(self, stream_name):
        self.client = boto3.client(
            'kinesis',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.stream_name = stream_name
        self.db = DatabaseQueries()
        
    def process_records(self):
        # Get shard iterator
        response = self.client.describe_stream(StreamName=self.stream_name)
        shard_id = response['StreamDescription']['Shards'][0]['ShardId']
        
        shard_iterator = self.client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=shard_id,
            ShardIteratorType='LATEST'
        )['ShardIterator']
        
        while True:
            response = self.client.get_records(
                ShardIterator=shard_iterator,
                Limit=100
            )
            
            for record in response['Records']:
                data = json.loads(record['Data'])
                if data['type'] == 'product':
                    self.db.insert_product(data['data'])
                elif data['type'] == 'user_behavior':
                    self.db.insert_user_behavior(data['data'])
                    
            shard_iterator = response['NextShardIterator']
            time.sleep(1)

if __name__ == "__main__":
    consumer = KinesisConsumer('ecommerce-stream')
    consumer.process_records()
