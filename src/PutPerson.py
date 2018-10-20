import os
import uuid
import json
import boto3
import traceback

print ('In PutPerson')

# Connect to DynamoDB Local
# For Mac:
ddb_table = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/").Table('PersonTable')

# For Windows:
# ddb = boto3.resource('dynamodb', endpoint_url="http://docker.for.windows.localhost:8000/").Table('PersonTable')

# For Linux:
# ddb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:8000").Table('PersonTable')


def lambda_handler(event, context):
    #print("Received event body: " + json.dumps(event, indent=2))

    # Load the JSON string into an object
    personData = json.loads(event['body'])

    # Generate ID for the item to be put
    PersonId = str(uuid.uuid4())

    # Put item
    try:
        ddb_table.put_item(
            Item={
                'Id': PersonId,
                'FirstName': personData['FName'],
                'LastName': personData['LName'],
                'Age': personData['Age']
            }
        )
    except:
        traceback.print_exc()
        return {'statusCode': 400, 'body': 'Error in putting item.'}

    else:
        # Echo back the Person ID as success status.
        return {'statusCode': 200, 'body': PersonId}  
    