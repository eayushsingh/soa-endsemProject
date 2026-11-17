import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FeedbackDB')

def lambda_handler(event, context):
    try:
        # Handle API Gateway Lambda proxy integration (body as string or dict)
        if 'body' in event and event['body']:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        # Extract fields
        feedback_id = str(body.get('FeedbackID'))
        student_name = body.get('StudentName')
        course_name = body.get('CourseName')
        rating = body.get('Rating')
        comments = body.get('Comments')
        
        # Validation
        if not feedback_id:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'FeedbackID is required'})
            }
        
        # Store item in DynamoDB
        item = {
            'FeedbackID': feedback_id,
            'StudentName': student_name,
            'CourseName': course_name,
            'Rating': rating,
            'Comments': comments
        }
        
        table.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Feedback submitted successfully!',
                'data': item
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
