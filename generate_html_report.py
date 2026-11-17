import base64
import os
import subprocess

workspace = "/Users/ayush/Desktop/soa-endsem"
screenshots_dir = os.path.join(workspace, "screenshots")

def get_base64_img(filename):
    path = os.path.join(screenshots_dir, filename)
    ext = os.path.splitext(filename)[1].lower().replace(".", "")
    mime = "image/png" if ext == "png" else "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

img_dynamo_created = get_base64_img("01_dynamodb_table_created.png")
img_iam_policy = get_base64_img("02_iam_role_policy.jpg")
img_submit_code = get_base64_img("03_submit_lambda_code.jpg")
img_get_created = get_base64_img("04_get_lambda_created.jpg")
img_get_code = get_base64_img("05_get_lambda_code.jpg")
img_api_created = get_base64_img("06_api_gateway_created.png")
img_api_resources = get_base64_img("07_api_gateway_resources.png")
img_api_dev = get_base64_img("08_api_gateway_dev_deployed.png")
img_dynamo_verified = get_base64_img("09_dynamodb_items_verified.jpg")
img_vscode = get_base64_img("10_vscode_source_code.jpg")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SOA Lab Practical Report - Ayush Singh</title>
<style>
  @page {{
    size: A4;
    margin: 15mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #24292e;
    line-height: 1.5;
    background: #fff;
    margin: 0;
    padding: 0;
    font-size: 13px;
  }}
  .header-card {{
    border: 2px solid #0969da;
    border-radius: 8px;
    padding: 16px 20px;
    background: #f6f8fa;
    margin-bottom: 20px;
  }}
  .header-title {{
    font-size: 20px;
    font-weight: 700;
    color: #0969da;
    text-align: center;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .header-subtitle {{
    font-size: 15px;
    font-weight: 600;
    text-align: center;
    color: #24292e;
    margin-bottom: 14px;
  }}
  .info-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 16px;
    border-top: 1px solid #d0d7de;
    padding-top: 12px;
    font-size: 13px;
  }}
  .info-item span.label {{
    font-weight: 600;
    color: #57606a;
  }}
  .info-item span.val {{
    font-weight: 700;
    color: #24292e;
  }}
  .github-badge {{
    grid-column: span 2;
    background: #e7f3ff;
    border: 1px solid #b6d3f2;
    padding: 8px 12px;
    border-radius: 6px;
    font-weight: 600;
    color: #0969da;
    word-break: break-all;
  }}
  h2 {{
    font-size: 16px;
    color: #0969da;
    border-bottom: 2px solid #eaeef2;
    padding-bottom: 5px;
    margin-top: 24px;
    margin-bottom: 12px;
  }}
  h3 {{
    font-size: 14px;
    color: #24292e;
    margin-top: 16px;
    margin-bottom: 8px;
  }}
  p, li {{
    color: #333;
    font-size: 12.5px;
  }}
  .screenshot-box {{
    margin: 12px 0 18px 0;
    text-align: center;
    page-break-inside: avoid;
  }}
  .screenshot-box img {{
    max-width: 98%;
    max-height: 380px;
    border-radius: 6px;
    border: 1px solid #d0d7de;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  }}
  .caption {{
    font-size: 11.5px;
    color: #57606a;
    font-style: italic;
    margin-top: 4px;
  }}
  pre {{
    background: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 10px;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
    font-size: 11px;
    overflow-x: auto;
    page-break-inside: avoid;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 12px;
    page-break-inside: avoid;
  }}
  table th, table td {{
    border: 1px solid #d0d7de;
    padding: 8px 10px;
    text-align: left;
  }}
  table th {{
    background: #f6f8fa;
    color: #24292e;
    font-weight: 600;
  }}
  .page-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<div class="header-card">
  <div class="header-title">Service Oriented Architecture (SOA) Lab Practical</div>
  <div class="header-subtitle">Serverless Feedback Management Application</div>
  <div class="info-grid">
    <div class="info-item"><span class="label">Student Name:</span> <span class="val">Ayush Singh</span></div>
    <div class="info-item"><span class="label">Roll Number:</span> <span class="val">2410080023</span></div>
    <div class="info-item"><span class="label">Serial / Assigned No:</span> <span class="val">16</span></div>
    <div class="info-item"><span class="label">AWS Region:</span> <span class="val">us-east-1 (N. Virginia)</span></div>
    <div class="github-badge">
      🔗 GitHub Repository: https://github.com/eayushsingh/soa-endsemProject
    </div>
  </div>
</div>

<h2>1. Aim & Objectives</h2>
<p>To design, implement, and deploy a fully scalable, event-driven <strong>Serverless Feedback Management Application</strong> on Amazon Web Services (AWS) that allows students to submit course feedback and retrieve previously submitted feedback using RESTful APIs, AWS Lambda, and Amazon DynamoDB.</p>

<h2>2. Architecture Overview</h2>
<pre>
Client (Curl/Postman) ──► Amazon API Gateway (/feedback) ──► AWS Lambda (Python 3.11) ──► Amazon DynamoDB (FeedbackDB)
  - POST /feedback: Submits feedback payload & stores into DynamoDB
  - GET  /feedback/{id}: Fetches feedback item by FeedbackID from DynamoDB
</pre>

<h2>3. Step 1: Create DynamoDB Table (FeedbackDB)</h2>
<p>Created a DynamoDB table named <strong>FeedbackDB</strong> with <strong>FeedbackID</strong> (String) as the Partition Key. Table status verified as <strong>Active</strong>.</p>
<div class="screenshot-box">
  <img src="{img_dynamo_created}" alt="DynamoDB Table Created">
  <div class="caption">Figure 1: DynamoDB Table 'FeedbackDB' created with Partition Key FeedbackID (Active).</div>
</div>

<div class="page-break"></div>

<h2>4. Step 2: IAM Role Configuration</h2>
<p>Configured an IAM Execution Role with <code>AmazonDynamoDBFullAccess</code> and <code>AWSLambdaBasicExecutionRole</code> policies to allow the Lambda functions to execute read/write operations on DynamoDB.</p>
<div class="screenshot-box">
  <img src="{img_iam_policy}" alt="IAM Role Policy Attached">
  <div class="caption">Figure 2: IAM Role with AmazonDynamoDBFullAccess policy successfully attached.</div>
</div>

<h2>5. Step 3 & 4: Implement Submit Feedback Lambda (SubmitFeedback)</h2>
<p>Implemented Lambda function in Python 3.11 to parse student feedback submissions (<code>FeedbackID</code>, <code>StudentName</code>, <code>CourseName</code>, <code>Rating</code>, <code>Comments</code>) and store them in DynamoDB via <code>put_item()</code>.</p>
<div class="screenshot-box">
  <img src="{img_submit_code}" alt="SubmitFeedback Lambda Deployed">
  <div class="caption">Figure 3: SubmitFeedback Lambda function code deployed successfully.</div>
</div>

<div class="page-break"></div>

<h2>6. Step 5: Implement Retrieve Feedback Lambda (GetFeedback)</h2>
<p>Created a second Lambda function in Python 3.11 to retrieve feedback details by path parameter <code>/feedback/{id}</code> using <code>get_item()</code> with automatic Decimal type serialization for JSON responses.</p>
<div class="screenshot-box">
  <img src="{img_get_created}" alt="GetFeedback Lambda Created">
  <div class="caption">Figure 4: Function GetFeedback created successfully.</div>
</div>
<div class="screenshot-box">
  <img src="{img_get_code}" alt="GetFeedback Lambda Code Deployed">
  <div class="caption">Figure 5: GetFeedback Lambda code updated and deployed.</div>
</div>

<div class="page-break"></div>

<h2>7. Step 6, 7 & 8: Build Amazon API Gateway & Integrate with Lambda</h2>
<p>Created REST API named <strong>FeedbackAPI</strong>. Configured endpoints:</p>
<ul>
  <li><code>POST /feedback</code>: Integrated with <code>SubmitFeedback</code> (Lambda Proxy Integration enabled)</li>
  <li><code>GET /feedback/{id}</code>: Integrated with <code>GetFeedback</code> (Lambda Proxy Integration enabled)</li>
</ul>
<div class="screenshot-box">
  <img src="{img_api_created}" alt="API Gateway Created">
  <div class="caption">Figure 6: REST API 'FeedbackAPI' created.</div>
</div>
<div class="screenshot-box">
  <img src="{img_api_resources}" alt="API Gateway Resources Configured">
  <div class="caption">Figure 7: Endpoints POST /feedback and GET /feedback/&#123;id&#125; configured.</div>
</div>

<div class="page-break"></div>

<h2>8. Step 9: Deploy API to Stage 'dev'</h2>
<p>The API was deployed to a stage named <strong>dev</strong>, generating the active Invoke URL: <code>https://jp36f93rp8.execute-api.us-east-1.amazonaws.com/dev</code>.</p>
<div class="screenshot-box">
  <img src="{img_api_dev}" alt="API Deployed to Stage dev">
  <div class="caption">Figure 8: FeedbackAPI deployed to stage 'dev' with active Invoke URL.</div>
</div>

<h2>9. Step 10: Endpoint Testing & JSON Responses</h2>
<h3>A. Submit Feedback Test (POST /feedback)</h3>
<pre>
curl -X POST https://jp36f93rp8.execute-api.us-east-1.amazonaws.com/dev/feedback \\
  -H "Content-Type: application/json" \\
  -d '{{"FeedbackID": "FB101", "StudentName": "Ayush Singh", "CourseName": "SOA", "Rating": 5, "Comments": "Great course and practical lab!"}}'

Response (HTTP 201 Created):
{{"message": "Feedback submitted successfully!", "data": {{"FeedbackID": "FB101", "StudentName": "Ayush Singh", "CourseName": "SOA", "Rating": 5, "Comments": "Great course and practical lab!"}}}}
</pre>

<h3>B. Retrieve Feedback Test (GET /feedback/FB101)</h3>
<pre>
curl -X GET https://jp36f93rp8.execute-api.us-east-1.amazonaws.com/dev/feedback/FB101

Response (HTTP 200 OK):
{{"StudentName": "Ayush Singh", "Comments": "Great course and practical lab!", "CourseName": "SOA", "Rating": 5, "FeedbackID": "FB101"}}
</pre>

<div class="page-break"></div>

<h2>10. Step 11: Verify Submitted Feedback in DynamoDB</h2>
<p>Verified that the submitted records are persisted in DynamoDB table <strong>FeedbackDB</strong> across multiple student entries:</p>

<table>
  <thead>
    <tr>
      <th>FeedbackID</th>
      <th>StudentName</th>
      <th>CourseName</th>
      <th>Rating</th>
      <th>Comments</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong>FB101</strong></td><td>Ayush Singh</td><td>SOA</td><td>5</td><td>Great course and practical lab!</td></tr>
    <tr><td><strong>FB102</strong></td><td>Rahul Sharma</td><td>Cloud Computing</td><td>4</td><td>Very informative session on AWS Lambda...</td></tr>
    <tr><td><strong>FB103</strong></td><td>Priya Patel</td><td>SOA</td><td>5</td><td>Hands-on experience with API Gateway...</td></tr>
    <tr><td><strong>FB104</strong></td><td>Amit Kumar</td><td>Distributed Systems</td><td>4</td><td>Good understanding of NoSQL database...</td></tr>
  </tbody>
</table>

<div class="screenshot-box">
  <img src="{img_dynamo_verified}" alt="DynamoDB Items Verified">
  <div class="caption">Figure 9: DynamoDB Explore Items showing multiple records persisted in FeedbackDB.</div>
</div>

<h2>11. Source Code Repository</h2>
<p>Complete project source code, report, test payloads, and instructions pushed to GitHub repository:</p>
<p><strong>GitHub URL:</strong> <a href="https://github.com/eayushsingh/soa-endsemProject">https://github.com/eayushsingh/soa-endsemProject</a></p>
<div class="screenshot-box">
  <img src="{img_vscode}" alt="VS Code Environment">
  <div class="caption">Figure 10: Local development environment and project files in VS Code.</div>
</div>

<h2>12. Conclusion</h2>
<p>All 11 requirements of the practical examination have been successfully implemented and validated. The serverless feedback application demonstrates zero-server maintenance, seamless auto-scaling, and secure API-to-database communication.</p>

</body>
</html>
"""

html_path = os.path.join(workspace, "report.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML report generated successfully at:", html_path)
