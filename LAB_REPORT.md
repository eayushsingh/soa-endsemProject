# Lab Practical Examination Report

**Student Name:** Ayush Singh  
**Sl. No. / Roll No:** 16  
**Subject:** Service Oriented Architecture (SOA) Lab Practical  
**Topic:** Serverless Application  
**Project Title:** Develop and Deploy a Serverless Feedback Management Application  

---

## 1. Aim / Objective
To design, develop, and deploy a fully serverless, highly scalable **Feedback Management Application** on Amazon Web Services (AWS) that allows students to submit course feedback and retrieve previously submitted feedback using RESTful API endpoints.

---

## 2. Serverless Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                  CLIENT (POSTMAN / CURL)                          |
+-----------------------------------------------------------------------------------+
                                   |                 ^
       POST /feedback (Submit)     |                 |  GET /feedback/{id} (Retrieve)
       JSON Payload                v                 |  JSON Response
+-----------------------------------------------------------------------------------+
|                           AMAZON API GATEWAY (REST API)                           |
|                      Invoke URL: https://jp36f93rp8.execute-api.us-east-1...     |
|                                   Stage: dev                                      |
+-----------------------------------------------------------------------------------+
                   |                                                 ^
                   | Proxy Integration                               | Proxy Integration
                   v                                                 |
+---------------------------------------+       +-----------------------------------+
|         AWS LAMBDA FUNCTION 1         |       |       AWS LAMBDA FUNCTION 2       |
|            SubmitFeedback             |       |            GetFeedback            |
|       (Processes & stores data)       |       |     (Fetches item by ID)          |
+---------------------------------------+       +-----------------------------------+
                   |                                                 ^
                   | put_item()                                      | get_item()
                   v                                                 |
+-----------------------------------------------------------------------------------+
|                              AMAZON DYNAMODB (NoSQL)                              |
|                              Table Name: FeedbackDB                               |
|                         Partition Key: FeedbackID (String)                        |
+-----------------------------------------------------------------------------------+
```

---

## 3. AWS Cloud Services Used
1. **Amazon DynamoDB**: Fully managed NoSQL key-value database used to persist feedback records.
2. **AWS Lambda**: Event-driven serverless compute service executing the Python application logic without provisioning servers.
3. **Amazon API Gateway**: Fully managed service allowing developers to create, publish, maintain, and monitor secure REST APIs.
4. **AWS Identity and Access Management (IAM)**: Used to grant least-privilege permissions (`AmazonDynamoDBFullAccess` and `AWSLambdaBasicExecutionRole`) to the execution roles.

---

## 4. Step-by-Step Implementation Procedure

### Step 1: Create DynamoDB Table
- **Table Name:** `FeedbackDB`
- **Partition Key:** `FeedbackID` (String)
- **Table Class:** Standard, on-demand capacity

### Step 2: Configure IAM Permissions
- Created/used execution role granting `AmazonDynamoDBFullAccess` and CloudWatch logging permissions so Lambda functions can interact with `FeedbackDB`.

### Step 3 & 4: Implement Submit Lambda Function (`SubmitFeedback`)
- Runtime: Python 3.11
- Parses JSON request body containing `FeedbackID`, `StudentName`, `CourseName`, `Rating`, and `Comments`.
- Executes `table.put_item(Item=item)` to persist data into DynamoDB.
- Returns HTTP `201 Created` with JSON confirmation.

### Step 5: Implement Retrieve Lambda Function (`GetFeedback`)
- Runtime: Python 3.11
- Extracts `id` from path parameters (`/feedback/{id}`).
- Executes `table.get_item(Key={'FeedbackID': str(feedback_id)})`.
- Handles Python `Decimal` serialization.
- Returns HTTP `200 OK` with retrieved feedback or HTTP `404 Not Found`.

### Step 6, 7 & 8: Build and Integrate Amazon API Gateway
- Created Regional REST API named `FeedbackAPI`.
- Configured Resource `/feedback` with method `POST` -> integrated with `SubmitFeedback` (Lambda Proxy Integration enabled).
- Configured Child Resource `/feedback/{id}` with method `GET` -> integrated with `GetFeedback` (Lambda Proxy Integration enabled).

### Step 9: Deploy API
- Deployed API to Stage: `dev`
- **Invoke Base URL:** `https://jp36f93rp8.execute-api.us-east-1.amazonaws.com/dev`

### Step 10 & 11: Testing & DynamoDB Verification
- Tested both endpoints with sample payloads via cURL / JSON requests.
- Verified persistent records inside DynamoDB console.

---

## 5. Source Code

### 5.1 Lambda Function 1: Submit Feedback (`submit_feedback.py`)
```python
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FeedbackDB')

def lambda_handler(event, context):
    try:
        if 'body' in event and event['body']:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        feedback_id = str(body.get('FeedbackID'))
        student_name = body.get('StudentName')
        course_name = body.get('CourseName')
        rating = body.get('Rating')
        comments = body.get('Comments')
        
        if not feedback_id:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'FeedbackID is required'})
            }
        
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
```

### 5.2 Lambda Function 2: Retrieve Feedback (`get_feedback.py`)
```python
import json
from decimal import Decimal
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FeedbackDB')

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
```

---

## 6. Execution & Test Results

### 6.1 Testing `POST /feedback`
**Request Command:**
```bash
curl -X POST https://jp36f93rp8.execute-api.us-east-1.amazonaws.com/dev/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "FeedbackID": "FB101",
    "StudentName": "Ayush Singh",
    "CourseName": "SOA",
    "Rating": 5,
    "Comments": "Great course and practical lab!"
  }'
```
**Response Output (HTTP 201 Created):**
```json
{
  "message": "Feedback submitted successfully!",
  "data": {
    "FeedbackID": "FB101",
    "StudentName": "Ayush Singh",
    "CourseName": "SOA",
    "Rating": 5,
    "Comments": "Great course and practical lab!"
  }
}
```

### 6.2 Testing `GET /feedback/{id}`
**Request Command:**
```bash
curl -X GET https://jp36f93rp8.execute-api.us-east-1.amazonaws.com/dev/feedback/FB101
```
**Response Output (HTTP 200 OK):**
```json
{
  "StudentName": "Ayush Singh",
  "Comments": "Great course and practical lab!",
  "CourseName": "SOA",
  "Rating": 5,
  "FeedbackID": "FB101"
}
```

---

## 7. DynamoDB Verification Table
Items successfully populated and verified in table **`FeedbackDB`**:

| FeedbackID | StudentName | CourseName | Rating | Comments |
| :--- | :--- | :--- | :---: | :--- |
| **FB101** | Ayush Singh | SOA | 5 | Great course and practical lab! |
| **FB102** | Rahul Sharma | Cloud Computing | 4 | Very informative session on AWS Lambda and Serverless. |
| **FB103** | Priya Patel | SOA | 5 | Hands-on experience with API Gateway was great. |
| **FB104** | Amit Kumar | Distributed Systems | 4 | Good understanding of NoSQL database concepts. |

---

## 8. Conclusion
The Serverless Feedback Management Application was successfully developed and deployed. By utilizing AWS Lambda, Amazon API Gateway, and Amazon DynamoDB, the application achieves high availability, automatic scaling, and a zero-server management footprint, fully satisfying all practical requirements.
