import json
import boto3
import os
import time

ec2 = boto3.resource('ec2', region_name=os.environ['REGION_NAME'])
ec2_client = boto3.client('ec2', region_name=os.environ['REGION_NAME'])

def lambda_handler(event, context):
    body = json.loads(event['body'])
    print(body)
    count = int(body['count'])
    data = {}

    try:
        instances = ec2.create_instances(
            ImageId=os.environ['IMAGE_ID'],
            MinCount=count,
            MaxCount=count,
            InstanceType=os.environ['INSTANCE_TYPE'],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'pi-flask-bot'
                        },
                    ]
                },
            ],
        )

        instance_ids = [i.instance_id for i in instances]
        print(instance_ids)

        time.sleep(15)

        a = ec2_client.describe_instances(
            InstanceIds=instance_ids
        )

        ips = []

        for r in a['Reservations']:
            for i in r['Instances']:
                ips.append(i['PublicIpAddress'])

        data['ips'] = ips
    except Exception as e:
        print(e)


    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({
            'data': data
        }),
    }
