import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('FamilyHappiness')

def lambda_handler(event, context):
    bucket = str(event['Records'][0]['s3']['bucket']['name'])
    key = str(event['Records'][0]['s3']['object']['key'])
    print bucket
    print key
    client=boto3.client('rekognition','us-east-1')
    response1=client.compare_faces(SimilarityThreshold=0,
                                  SourceImage={'S3Object':{'Bucket':bucket,'Name':key}},
                                  TargetImage={'S3Object':{'Bucket':'sensorfamilyphotos','Name':'Chen.jpg'}})
    response2=client.compare_faces(SimilarityThreshold=0,
                                  SourceImage={'S3Object':{'Bucket':bucket,'Name':key}},
                                  TargetImage={'S3Object':{'Bucket':'sensorfamilyphotos','Name':'Luo.jpg'}})
    response3=client.compare_faces(SimilarityThreshold=0,
                                  SourceImage={'S3Object':{'Bucket':bucket,'Name':key}},
                                  TargetImage={'S3Object':{'Bucket':'sensorfamilyphotos','Name':'Zhu.jpg'}})   
             
    simi1 = int(response1['FaceMatches'][0]['Similarity'])
    simi2 = int(response2['FaceMatches'][0]['Similarity'])
    simi3 = int(response3['FaceMatches'][0]['Similarity'])
    
    print simi1
    print simi2
    print simi3
    
    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':key}},Attributes=['ALL'])
    
    print response['FaceDetails'][0]['Emotions']
    for emo in response['FaceDetails'][0]['Emotions']:
        if emo['Type']=='HAPPY' and int(emo['Confidence'])>80:
            print 'happy inside'
            if simi1 > simi2 and simi1 > simi3:
                table.delete_item(
                    Key={
                        'username': 'chen'
                    }
                )
                table.put_item(
                    Item={
                        'username': 'chen',
                        'Happiness': 'HAPPY',
                    }
                )
            elif simi2 > simi1 and simi2 > simi3:
                table.delete_item(
                    Key={
                        'username': 'luo'
                    }
                )
                table.put_item(
                    Item={
                        'username': 'luo',
                        'Happiness': 'HAPPY',
                    }
                )
            elif simi3 > simi1 and simi3 > simi2:
                table.delete_item(
                    Key={
                        'username': 'zhu'
                    }
                )
                table.put_item(
                    Item={
                        'username': 'zhu',
                        'Happiness': 'HAPPY',
                    }
                )
        elif emo['Type']=='HAPPY' and int(emo['Confidence'])>50:
            print 'medium inside'
            if simi1 > simi2 and simi1 > simi3:
                table.delete_item(
                    Key={
                        'username': 'chen'
                    }
                )
                table.put_item(
                    Item={
                        'username': 'chen',
                        'Happiness': 'Medium',
                    }
                )
            elif simi2 > simi1 and simi2 > simi3:
                table.delete_item(
                    Key={
                        'username': 'luo'
                    }
                )
                table.put_item(
                    Item={
                        'username': 'luo',
                        'Happiness': 'Medium',
                    }
                )
            elif simi3 > simi1 and simi3 > simi2:
                table.delete_item(
                    Key={
                        'username': 'zhu'
                    }
                )
                table.put_item(
                    Item={
                        'username': 'zhu',
                        'Happiness': 'Medium',
                    }
                )
        elif emo['Type']=='HAPPY':
            print 'unhappy inside'
            if simi1 > simi2 and simi1 > simi3:
                table.delete_item(
                    Key={
                        'username': 'chen'
                    }
                )
                table.put_item(
                    Item={
                        'username': 'chen',
                        'Happiness': 'UNHAPPY',
                    }
                )
            elif simi2 > simi1 and simi2 > simi3:
                table.delete_item(
                    Key={
                        'username': 'luo'
                    }
                )
                table.put_item(
                    Item={
                        'username': 'luo',
                        'Happiness': 'UNHAPPY',
                    }
                )
            elif simi3 > simi1 and simi3 > simi2:
                table.delete_item(
                    Key={
                        'username': 'zhu'
                    }
                )
                table.put_item(
                    Item={
                        'username': 'zhu',
                        'Happiness': 'UNHAPPY',
                    }
                )
    return 'Hello from Lambda'
