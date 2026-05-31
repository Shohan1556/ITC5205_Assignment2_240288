## Name: Abu Tawhid Shohan
## Student ID: 240288
## Subject: ITC5205 -- Cloud Computing
## Institution: Apex Australia Higher Education

## Project: AWS Serverless Image Object Detection System

## Description:
A fully serverless image object detection pipeline built on AWS.
Images stored in Amazon S3 are analysed using Amazon Rekognition
(detect_labels API), triggered via AWS Lambda through Amazon API
Gateway (REST API). Detection results are stored back to S3 as JSON
files and recorded in Amazon DynamoDB for audit and retrieval.
The system is secured with API key authentication via a Usage Plan
and monitored via Amazon CloudWatch Logs and Metrics.

## AWS Services Used:
- AWS IAM (execution role and permissions)
- Amazon S3 (image input and result storage)
- Amazon DynamoDB (detection metadata storage)
- AWS Lambda (Python 3.12, serverless compute)
- Amazon Rekognition (deep learning object detection)
- Amazon API Gateway (REST API, prod stage)
- Amazon CloudWatch (logging and metrics)

## Live API Endpoint:
https://hz3u9ymr75.execute-api.us-east-1.amazonaws.com/prod/detect

### Method: POST
Required Header: x-api-key: <API_KEY>
Request Body: {"image_key": "input-images/<filename>.jpg"}

### Region: us-east-1 (N. Virginia)
