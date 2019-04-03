import os
import uuid
import json
import boto3
import traceback
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    # Get environment variables
    table_name = os.environ['TABLE']
    region = os.environ['REGION']
    aws_environment = os.environ['AWSENV']
    dev_environment = os.environ['DEVENV']

    # Check if executing locally or on AWS, and configure DynamoDB connection accordingly.
    if aws_environment == "AWS_SAM_LOCAL":
        # SAM LOCAL
        if dev_environment == "OSX":
            # Environment ins Mac OSX
            person_table = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/").Table(table_name)

        elif dev_environment == "Windows":
            # Environment is Windows
            person_table = boto3.resource('dynamodb', endpoint_url="http://docker.for.windows.localhost:8000/").Table(table_name)

        else:
            # Environment is Linux
            person_table = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:8000").Table(table_name)
    else:
        # AWS
        person_table = boto3.resource('dynamodb', region_name=region).Table(table_name)


    # Load body JSON for processing
    try:
        bodydict = json.loads(event['body'])
    except:
        return {'statusCode': 400, 'body': 'malformed JSON'}

    # GET Method
    if event['httpMethod'] == 'GET':
        print("In GET method")

        try:
            response = person_table.get_item(
                Key={'Id': bodydict['Id']}
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return {'statusCode': 400, 'body': e.response['Error']['Message']}
        else:
            item = response['Item']
            print("GetItem succeeded:")
            resp = item['FirstName'] + ' ' + item['LastName'] + ' ' + str(item['Age'])
            return {'statusCode': 200, 'body': resp}

    # POST Method
    elif event['httpMethod'] == 'POST':
        # Check for missing information in the request.
        if ('FName' not in event['body']) or not(bodydict["FName"]):
            return {'statusCode': 400, 'body': 'missing person first name.'}
        if ('LName' not in bodydict) or not(bodydict["LName"]):
            return {'statusCode': 400, 'body': 'missing person last name.'}
        if ('Age' not in event['body']) or not(bodydict["Age"]):
            return {'statusCode': 400, 'body': 'missing person age.'}

        # Write to DynamoDB table
        # Generate ID for the item to be put
        PersonId = str(uuid.uuid4())

        # Put item in the DynamoDB table
        try:
            person_table.put_item(
			    Item={
				    'Id': PersonId,
                    'FirstName': bodydict["FName"],
                    'LastName': bodydict["LName"],
                    'Age': bodydict["Age"]
                }
            )
        except:
            traceback.print_exc()
            return {'statusCode': 400, 'body': 'Error in putting item.'}
        else:
            print ('Item inserted')
            # Echo back the Person ID as success message.
            return {'statusCode': 200, 'body': PersonId}  

