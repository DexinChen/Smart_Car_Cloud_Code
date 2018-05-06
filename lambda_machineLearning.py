import boto3

client = boto3.client('machinelearning')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('FamilyHappiness')

def lambda_handler(event, context):
    # TODO implement
    response = client.predict(
        MLModelId='ml-pkMBETyVcmM',
        Record={
            'Username (S)': event['params']['querystring']['Username'],
            'Gravity (S)': event['params']['querystring']['Gravity'],
            'Gyroscope (S)': event['params']['querystring']['Gyroscope'],
            'Light (S)': event['params']['querystring']['Light'],
            'Magnetic Field (S)': event['params']['querystring']['MagneticField'],
            'Pressure (S)': event['params']['querystring']['Pressure'],
            'Proximity (S)': event['params']['querystring']['Proximity'],
            'Accelerometer (S)': event['params']['querystring']['Accelerometer']
        },
        PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'
    )
    label1 = response['Prediction']['predictedLabel']
    if label1 == 'Yes':
        label1 = 'HAPPY'
    elif label1 == 'Medium':
        label1 = 'MEDIUM'
    else:
        label1 = 'UNHAPPY'
    response = table.get_item(
        Key={
            'username': event['params']['querystring']['Username']
        }
    )
    item = response['Item']
    label2 = item['Happiness']
    res = 'Photo Result: '+label2 + ', ' +'ML Result: '+label1
    return res
