import json
import boto3
from database.queries import DatabaseQueries

def lambda_handler(event, context):
    db = DatabaseQueries()
    
    for record in event['Records']:
        payload = json.loads(record['kinesis']['data'])
        
        try:
            if payload['type'] == 'product':
                db.insert_product(payload['data'])
            elif payload['type'] == 'user_behavior':
                db.insert_user_behavior(payload['data'])
                
            print(f"Successfully processed record: {record['kinesis']['sequenceNumber']}")
        except Exception as e:
            print(f"Error processing record: {e}")
            raise e
            
    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed successfully')
    }
