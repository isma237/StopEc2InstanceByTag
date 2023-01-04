import json
import logging
import boto3

# import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')


def stop_instance(instance):
    try:
        response = client.stop_instances(
            InstanceIds=[instance.id]
        )
        format_response(response)

    except Exception as e:
        logger.error(e)
        raise e


def format_response(response):
    logger.info(response)


def lambda_handler(event, context):

    try:
        # retrieve all instances with specific tag and value
        instances = ec2.instances.filter(
            Filters=[
                {
                    'Name': 'tag:Project',
                    'Values': ['Lab_Test'],
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )

        for instance in instances:
            stop_instance(instance)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }),
        }

    except Exception as error:
        logger.error(error)
        return
