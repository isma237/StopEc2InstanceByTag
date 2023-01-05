import json
import logging
import boto3
import os
from tabulate import tabulate

# import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
senderEmail = os.environ['senderEmail']
receiverEmail = os.environ['receiverEmail']


def stop_instance(instance):
    try:
        client.stop_instances(
            InstanceIds=[instance.id]
        )
    except Exception as e:
        logger.error(e)
        raise e


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
        informations = []
        for instance in instances:
            stop_instance(instance)
            informations.append([instance.id, 'Stopping'])

        client = boto3.client('ses')
        client.send_email(Source=senderEmail,
                          Destination={'ToAddresses': [receiverEmail]},
                          Message={
                              'Subject': {
                                  'Data': 'Action programmée: Arrêt des instances',
                                  'Charset': 'utf-8'
                              },
                              'Body': {
                                  'Text': {
                                      'Data': tabulate(informations, headers=['Instance Id', 'Status']),
                                      'Charset': 'utf-8'
                                  }
                              }
                          }
                          )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "traitement terminé. Un rapport sera envoyé par mail"
            }),
        }

    except Exception as error:
        logger.error(error)
        return
