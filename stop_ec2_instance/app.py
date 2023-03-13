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
ses = boto3.client('ses')

senderEmail = os.environ['senderEmail']
receiverEmail = os.environ['receiverEmail']

keys = os.environ['tagKeysList'].strip().split(',')
values = os.environ['tagValuesList'].strip().split(',')


def stop_instance(instance):
    try:
        client.stop_instances(
            InstanceIds=[instance.id]
        )
    except Exception as e:
        logger.error(e)
        raise e


def format_tag():
    if len(keys) != len(values):
        raise IndexError("Erreur: Les variables des TagKeysList et des TagValuesList "
                         "qui permettent de définir les TAGS ne "
                         "contiennent pas le même nombre d'éléments")

    tags = []
    for i in range(0, len(keys)):
        key = keys[i]
        value = values[i]

        tags.append({
            'Name': f'tag:{key}',
            'Values': [value]
        })

    return tags


def lambda_handler(event, context):
    try:
        # retrieve all instances with specific tag and value
        filters = format_tag()

        filters.append({
            'Name': 'instance-state-name',
            'Values': ['running']
        })

        instances = ec2.instances.filter(Filters=filters)

        informations = []
        size = 0
        for instance in instances:
            stop_instance(instance)
            size = size + 1
            informations.append([instance.id, 'Stopping'])

        object = 'Tâche planifiée:: Arrêt des instances: Opération terminée avec succès'
        if size != 0:
            data = tabulate(informations, headers=['Instance Id', 'Status'])
            sendMail(senderEmail, receiverEmail, object, data)
        else:
            data = "Aucune instance repondant aux critères définis n'est en cours d'exécution actuellement"

        logger.info(data)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "traitement terminé. Un rapport sera envoyé par mail"
            }),
        }
    except IndexError:
        errorMessage = f'Un problème est survénu durant le traitement. \nLe nombre de clés et de valeurs définissant ' \
                       f'les tags passés en paramètères doivent être identiques. \n\n\n' \
                       f'Tableau des clés:\t {tabulate(keys)} \n\nTableau des valeurs:\t {tabulate(values)}'

        logger.error(errorMessage)
        object = 'Tâche planifiée:: Arrêt des instances: Opération interrompue'

        sendMail(senderEmail, receiverEmail, object, errorMessage)
        return {
            "statusCode": 300,
            "error": "Impossible de terminer l'opération",
        }

    except Exception as error:
        logger.error(error)
        return {
            "statusCode": 300,
            "error": json.dumps({
                "message": error
            }),
        }


def sendMail(senderEmail, receiverEmail, object, data):
    ses.send_email(Source=senderEmail,
                   Destination={'ToAddresses': [receiverEmail]},
                   Message={
                       'Subject': {
                           'Data': object,
                           'Charset': 'utf-8'
                       },
                       'Body': {
                           'Text': {
                               'Data': data,
                               'Charset': 'utf-8'
                           }
                       }
                   }
                   )
