import json
from decimal import Decimal
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FeedbackDB')

# Helper to convert DynamoDB Decimal types to int/float for JSON serialization
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def lambda_handler(event, context):
    try:
        feedback_id = None
        if 'pathParameters' in event and event['pathParameters']:
            feedback_id = event['pathParameters'].get('id')
        elif 'id' in event:
            feedback_id = event.get('id')
        elif 'FeedbackID' in event:
            feedback_id = event.get('FeedbackID')
            
        if not feedback_id:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'id parameter is required'})
            }
        
        response = table.get_item(Key={'FeedbackID': str(feedback_id)})
        item = response.get('Item')
        
        if not item:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': f'Feedback with ID {feedback_id} not found'})
            }
            
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(item, default=decimal_default)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
