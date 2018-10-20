import os
import uuid
import json
import boto3
import traceback

print ('In GetPerson')

# Connect to DynamoDB Local
# For Mac:
ddb_table = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/").Table('PersonTable')

# For Windows:
# ddb_table = boto3.resource('dynamodb', endpoint_url="http://docker.for.windows.localhost:8000/").Table('PersonTable')

# For Linux:
# ddb_table = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:8000").Table('PersonTable')


def lambda_handler(event, context):
    print("Received event body: " + json.dumps(event, indent=2))

    # Generate ID for the item to be put
    PersonId = event['body']
    print('Person ID is: ' + PersonId)

    # Put item
    try:
        result = ddb_table.get_item(
            Key={
                'Id': PersonId
            }
        )
    except:
        traceback.print_exc()
        return {'statusCode': 400, 'body': 'Error in retrieving item.'}  
    
    else:
        item = result['Item']

        response = item['FirstName'] + ' ' + item['LastName'] + ' ' + str(item['Age'])
        print(item['FirstName'])

        # Return person details.
        return {'statusCode': 200, 'body': response}  
    