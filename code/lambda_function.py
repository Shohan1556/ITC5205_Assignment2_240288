import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    table_name = os.environ['DYNAMODB_TABLE']

    # Get image key from event
    body = json.loads(event.get('body', '{}'))
    image_key = body.get('image_key')

    if not image_key:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'image_key is required'})
        }

    try:
        # Run Rekognition object detection
        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': image_key}},
            MaxLabels=10,
            MinConfidence=70
        )

        labels = [
            {'name': label['Name'], 'confidence': round(label['Confidence'], 2)}
            for label in response['Labels']
        ]

        timestamp = datetime.utcnow().isoformat()
        image_id = image_key.split('/')[-1].replace('.', '_')

        # Save result JSON to S3 detection-results/
        result_key = f"detection-results/{image_id}_{timestamp}.json"
        result_data = {
            'image_id': image_id,
            'timestamp': timestamp,
            'source_image': image_key,
            'detected_labels': labels
        }

        s3.put_object(
            Bucket=bucket_name,
            Key=result_key,
            Body=json.dumps(result_data, indent=2),
            ContentType='application/json'
        )

        # Save record to DynamoDB
        table = dynamodb.Table(table_name)
        table.put_item(Item={
            'image_id': image_id,
            'timestamp': timestamp,
            'source_image': image_key,
            'detected_labels': json.dumps(labels),
            'result_s3_key': result_key
        })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Detection complete',
                'image_id': image_id,
                'labels_detected': len(labels),
                'labels': labels,
                'result_saved_to': result_key
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
