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
2. Avoir un bucket S3 dans lequel seront stockés les artefacts générés par les builds de l'application SAM. Ce bucket 
sera utilisé lors de la 5ième étape du processus de lancement. 


## Fonctionnement

Pour fonctionner vous devez définir les variables suivantes lors du déploiement du stack.

- **CronPlanification** Permet de définir la fréquence d'exécution de lancement du programme: 
- **SenderEmailAddress:** Adresse email de l'emetteur - cette adresse email doit être validée sur SES
- **ReceiverEmailAddress:** Adresse email de la personne qui sera notifiée après le traitement
- **SESIdentitySenderUser:** ARN du SES Identity de l'adresse email de l'émeteur
- **TagKeysList:** Liste des clés des TAGS séparées par des virgules __ NB Le nombre doit êre identique à celui de la variable TagValuesList. Exemple key1,key2
- **TagValuesList:** Liste des valeurs des TAGS séparées par des virgules __ NB -- Le nombre doit êre identique à celui de la variable TagKeysList Exemple tag1,tag2
- **EventBridgeName:** Nom du service EventBridge

## Comment déployer son stack
Nous verrons comment déployer son stack SAM à partir de Cloud9, l'IDE disponible sur AWS.\
Vous pouvez également le faire en utilisan SAM CLI. [Cliquez ici](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) pour accéder à la documentation officielle. 
Le tutoriel suivant vous aidera à pendre la main rapidement: [Hello Worl Tutorial](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html).

### Les étapes à suivre
1. Créer un environnement Cloud9 en suivant le [lien](https://docs.aws.amazon.com/cloud9/latest/user-guide/tutorial-create-environment.html). Vérifier que vous utilisez une instance de type t2.micro pour profiter de l'offre free tiers
2. Clôner le projet à l'aide de la commande `git clone repository_https_url`
3. Changer de repertoire: `cd StopEc2InstanceByTag`
4. Créer un fichier dans lequel seront stockées les variables
   - `touch .aws/template.json` et coller le contenu ci-dessous
   ```
   {
        "templates": {
            "template.yaml": {
                "parameterOverrides": {
                     "CronPlanification": "cron(30 19 * * *)",
                     "TagKeysList": "Project",
                     "TagValuesList": "LAB_TEST",
                     "EventBridgeDescription": "Sample Description",
                     "EventBridgeName": "CallerStopEC2Instances"
                }
            }
        }
   }
   ```
5. Sur la gauche, cliquez sur l'icône AWS de cloud9
6. Faites un clique droit sur Lambda et sélectionner **Deploy SAM Application**. Vous pouvez ensuite suivre les étapes 


