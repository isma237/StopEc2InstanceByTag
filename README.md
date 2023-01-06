# StopEc2InstancesByTagsDefinition
### Pourquoi ?
Est-ce qu'il vous arrive aussi d'oublier d'éteindre vos instances 
EC2 après avoir réalisé des labs sur AWS ?


Si comme moi, vous vous en voulez après avoir laisser plusieurs 
instances tourner inutilement alors ce projet pourrait vous interesser. 

Cette application construite sur la base de SAM (Serverless Application 
Model) vous permettra de **planifier l'arrêt** des instances **sélectionnées
sur la base de TAG**. 

L'utilisation des TAG permet d'apporter des informations supplémentaires à vos
ressources sur AWS. Une fois maitriser, ce sera un compagnon idéal pour gérer des grosses infrastructures.
Vous pouvez en apprendre plus en suivant le lien suivant [Tagging AWS resources](https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html)


## Prérequis

1. Avoir un compte sur AWS
2. AWS CLI configuré. Vous pouvez suivre ce tutoriel [Installer et configurer AWS CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
3. Configurer AWS CLI avec un compte utilisateur possédant les droits de création et d'éxécution des
services suivants:
   1. AWS LAMBDA
   2. AWS SES
   3. AWS EventBridge
   4. AWS IAM
4. Créer un bucket S3 et utiliser le nom de ce bucket dans la commande deploy à la place de **bucket_name**


## Fonctionnement

Pour fonctionner vous devez fournir les variables suivantes lors du déploiement du stack.

- **SenderEmailAddress:** Adresse email de l'emetteur - cette adresse email doit être validée sur SES
- **ReceiverEmailAddress:** Adresse email de la personne qui sera notifiée après le traitement
- **SESIdentitySenderUser:** ARN du SES Identity de l'adresse email de l'émeteur
- **TagKeysList:** Liste des clés des TAGS séparées par des virgules __ NB Le nombre doit êre identique à celui de la variable TagValuesList. Exemple key1,key2
- **TagValuesList:** Liste des valeurs des TAGS séparées par des virgules __ NB -- Le nombre doit êre identique à celui de la variable TagKeysList Exemple tag1,tag2
- **EventBridgeName:** Nom du service EventBridge

## Les étapes
Après avoir cloné le projet, il faudra suivre les étapes suivantes:

1. Installer SAM CLI sur votre ordinateur [Installation de SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
3. Builder le projet: `sam build`
4. Déployer la solution: 
`sam deploy --template-file ./.aws-sam/build/packaged-template.yaml --stack-name StopEc2InstanceByTags --s3-bucket bucket_name --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --no-execute-changeset --parameter-overrides SenderEmailAddress=senderEmailVariable ReceiverEmailAddress=receiverEmailVariable SESIdentitySenderUser=SesIdentityArnOfSenderEmail TagKeysList=key1,key2 TagValuesList=value1,value2 EventBridgeName=CallerStopEC2Instances EventBridgeDescription="Sample Description"`


Vous pouvez également suivre le tutoriel d'introduction à SAM et l'appliquer à ce projet.
[Hello Worl Tutorial](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)
