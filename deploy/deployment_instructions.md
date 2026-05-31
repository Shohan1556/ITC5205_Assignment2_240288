================================================================

DEPLOYMENT INSTRUCTIONS

ITC5205 Assignment 2 -- AWS Serverless Image Object Detection

Student: Abu Tawhid Shohan (240288)

================================================================



**PRE-REQUISITES**

\--------------

\- AWS account with console access

\- Region: us-east-1 (N. Virginia)

\- AWS CloudShell or curl installed for testing



\----------------------------------------------------------------

**STEP 1 -- IAM Role**

\----------------------------------------------------------------

1\. Go to IAM > Roles > Create role

2\. Trusted entity: AWS service > Lambda

3\. Attach the following managed policies:

&#x20;  - AmazonS3FullAccess

&#x20;  - AmazonDynamoDBFullAccess

&#x20;  - AmazonRekognitionFullAccess

&#x20;  - AWSLambdaBasicExecutionRole

4\. Role name: yolov5-detection-role

5\. Click Create role



\----------------------------------------------------------------

**STEP 2 -- Amazon S3 Bucket**

\----------------------------------------------------------------

1\. Go to S3 > Create bucket

2\. Bucket name: yolov5-detection-<your-student-id>

3\. Region: us-east-1

4\. Keep Block Public Access enabled

5\. Create bucket

6\. Inside bucket, create two folders:

&#x20;  - input-images/

&#x20;  - detection-results/

7\. Upload test images (JPEG) to input-images/



\----------------------------------------------------------------

**STEP 3 -- Amazon DynamoDB Table**

\----------------------------------------------------------------

1\. Go to DynamoDB > Create table

2\. Table name: DetectionResults

3\. Partition key: image\_id (String)

4\. Sort key: timestamp (String)

5\. Table settings: Customize settings

6\. Table class: DynamoDB Standard

7\. Capacity mode: On-demand

8\. Click Create table

9\. Wait for status: Active



\----------------------------------------------------------------

**STEP 4 -- AWS Lambda Function**

\----------------------------------------------------------------

1\. Go to Lambda > Create function > Author from scratch

2\. Function name: yolov5-detection-function

3\. Runtime: Python 3.12

4\. Architecture: x86\_64

5\. Permissions: Use existing role > yolov5-detection-role

6\. Click Create function

7\. Go to Configuration > General configuration > Edit:

&#x20;  - Memory: 512 MB

&#x20;  - Timeout: 1 min 0 sec

&#x20;  - Save

8\. Go to Configuration > Environment variables > Edit:

&#x20;  - Add: BUCKET\_NAME = yolov5-detection-<your-student-id>

&#x20;  - Add: DYNAMODB\_TABLE = DetectionResults

&#x20;  - Save

9\. Go to Code tab, open lambda\_function.py

10\. Delete existing code, paste contents of code/lambda\_function.py

11\. Click Deploy



\----------------------------------------------------------------

**STEP 5 -- Test Lambda Directly**

\----------------------------------------------------------------

1\. Go to Test tab > Create new event

2\. Event name: TestDetection

3\. Event JSON:

&#x20;  {

&#x20;    "body": "{\\"image\_key\\": \\"input-images/1.jpg\\"}"

&#x20;  }

4\. Save and click Test

5\. Expected: Execution succeeded, statusCode 200

6\. Verify: S3 detection-results/ has new JSON file

7\. Verify: DynamoDB DetectionResults has new item



\----------------------------------------------------------------

**STEP 6 -- Amazon API Gateway**

\----------------------------------------------------------------

1\. Go to API Gateway > Create API > REST API > Build

2\. API name: yolov5-detection-api

3\. Endpoint type: Regional

4\. Create API

5\. Click Create resource:

&#x20;  - Resource name: detect

&#x20;  - Resource path: /detect

&#x20;  - Create resource

6\. With /detect selected, click Create method:

&#x20;  - Method type: POST

&#x20;  - Integration type: Lambda function

&#x20;  - Enable Lambda proxy integration: ON

&#x20;  - Lambda function: yolov5-detection-function (us-east-1)

&#x20;  - Create method

7\. Click Deploy API:

&#x20;  - Stage: \*New stage\*

&#x20;  - Stage name: prod

&#x20;  - Deploy

8\. Copy the Invoke URL shown on the prod stage page



\----------------------------------------------------------------

**STEP 7 -- API Key and Usage Plan**

\----------------------------------------------------------------

1\. Go to API Keys > Create API key:

&#x20;  - Name: yolov5-api-key

&#x20;  - Auto generate

&#x20;  - Save

&#x20;  - Note the generated key value



2\. Go to Usage Plans > Create usage plan:

&#x20;  - Name: yolov5-usage-plan

&#x20;  - Rate: 100 requests/second

&#x20;  - Burst: 50

&#x20;  - Quota: 10000 requests/month

&#x20;  - Create



3\. Inside usage plan > Add stage:

&#x20;  - API: yolov5-detection-api

&#x20;  - Stage: prod

&#x20;  - Add to usage plan



4\. Inside usage plan > Associated API keys > Add API key:

&#x20;  - Select: yolov5-api-key

&#x20;  - Add API key



5\. Go back to API > Resources > /detect > POST > Method request > Edit:

&#x20;  - API key required: checked (true)

&#x20;  - Save



6\. Click Deploy API again:

&#x20;  - Stage: prod

&#x20;  - Deploy



\----------------------------------------------------------------

**STEP 8 -- Test Full Pipeline via CloudShell**

\----------------------------------------------------------------

Open AWS CloudShell and run:



curl -X POST \\

&#x20; https://<your-api-id>.execute-api.us-east-1.amazonaws.com/prod/detect \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -H "x-api-key: <YOUR\_API\_KEY>" \\

&#x20; -d '{"image\_key": "input-images/1.jpg"}'



Expected response:

{

&#x20; "message": "Detection complete",

&#x20; "image\_id": "1\_jpg",

&#x20; "labels\_detected": 7,

&#x20; "labels": \[...],

&#x20; "result\_saved\_to": "detection-results/1\_jpg\_<timestamp>.json"

}



\----------------------------------------------------------------

**TROUBLESHOOTING**

\----------------------------------------------------------------

\- 403 Forbidden     : Missing or incorrect x-api-key header

\- 400 Bad Request   : Missing image\_key in request body

\- 500 Server Error  : Image not found in S3 or wrong format

&#x20;                     Check CloudWatch > Log groups >

&#x20;                     /aws/lambda/yolov5-detection-function

================================================================



