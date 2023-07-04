import json
import logging
import boto3
from datetime import timedelta
from datetime import datetime

sm_client = boto3.Session().client('sagemaker-runtime')
qs_client = boto3.client('quicksight')
    
def lambda_handler(event, context):
    now = datetime.now()
    korea_time = now + timedelta(hours=9)
    timestamp = korea_time.strftime("%m/%d/%Y %H:%M:%S")
    print(timestamp)

    sentence_id          = event['id']
    sentence    = event['sentence']
    
    endpoint_name = 'KorNLPServerlessEndpoint-nsmc-2023-07-02-10-45-02'

    input_txt = "{\"text\": \"" + sentence +"\"}"
    
    with open('/tmp/test.txt', 'w') as file:
        file.write(input_txt) 

    with open('/tmp/test.txt', mode='rb') as file:
        model_input_data = file.read()  
        
    """
    with open('/tmp/test.txt', 'rb') as file:
        model_input_data = file.read()  
    """

    model_response = sm_client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/jsonlines",
        Accept="application/jsonlines",
        Body=model_input_data
    )
    
    model_outputs = model_response['Body'].read().decode()
    model_outputs_json = json.loads(model_outputs)
    """ {"predicted_label": "Pos", "score": 0.7344177961349487} """
    predicted_label = model_outputs_json["predicted_label"]
    score           = model_outputs_json["score"]


    ddb_client = boto3.client('dynamodb')
    
    ddb_response = ddb_client.put_item(
        TableName='ratings',
        Item={
            'id': {
                'S': sentence_id,
                },
            'sentence': {
                'S': sentence
                },
            'predicted_label': {
                'S': predicted_label
                },
            'score': {
                'N': str(score)
                },
            'datetime': {
                'S': timestamp
            }
        })
    
    
    
    qs_response = qs_client.create_ingestion(
                    AwsAccountId="{account-id}",
                    DataSetId='37e42416-0e87-41fa-b6fa-5540408316a9',
                    IngestionId=datetime.now().strftime("%d%m%y-%H%M%S-%f"),
            )
    
    return qs_response
