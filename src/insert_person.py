import os
import uuid
import json
import boto3

if os.getenv("AWS_SAM_LOCAL"):
    person_table = boto3.resource(
        'dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/"
    ).Table("PersonTable")
else:
    person_table = boto3.resource('dynamodb', region_name='us-west-2').Table("PersonTable")

def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'GET':
        try:
            response = table.get_item(
                Key={'Id': event['body']['Id']}
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            item = response['Item']
            print("GetItem succeeded:")
            print(json.dumps(item, indent=4, cls=DecimalEncoder))

        #resp = person_table.scan()
        return {'body': json.dumps(item)}
    elif event['httpMethod'] == 'POST':
        try:
            body = json.loads(event['body'])
        except:
            return {'statusCode': 400, 'body': 'malformed json input'}
        if 'person' not in body:
            return {'statusCode': 400, 'body': 'missing person details in request body'}

        print (body)

        # Write to DynamoDB table
        resp = person_table.put_item(
			Person = {
				'Id': str(uuid.uuid4()),
                'FName': body['FName'],
                'LName': body['LName'],
                'Age': body['Age']
            }
        )
        print ('Item inserted')
        print(json.dumps(resp, indent=4, cls=DecimalEncoder))
