
# Digitruc: StopEc2InstancesByTagsDefinition

### Pourquoi ?
Si comme moi, il vous arrive d'oublier d'arrêter d'éteindre 
vos instances EC2 après avoir terminé des labs, alors ce projet pourrait vous interesser. 

Cette application construite sur la base de SAM (Serverless Application 
Model) vous permettra de **planifier l'arrêt** des instances **sélectionnées
sur la base des TAGS**. 

Les TAGS permettent d'apporter des informations supplémentaires à vos ressources sur AWS. 
Une fois maitrisé, ce sera un compagnon idéal pour gérer des grosses infrastructures.
Vous pouvez en apprendre plus en suivant le lien suivant [Tagging AWS resources](https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html)


## Prérequis

1. Avoir un compte sur AWS
2. Avoir un bucket S3 dans lequel seront stockés les artefacts générés par les builds de l'application SAM. Ce bucket 
sera utilisé dans la dernière étape du processus de lancement. 


## Fonctionnement

Pour fonctionner vous devez définir les variables suivantes lors du déploiement du stack.

- **CronPlanification** Permet de définir la fréquence d'exécution de lancement du programme: 
- **SenderEmailAddress:** Adresse email de l'émetteur - cette adresse email doit être créée et validée sur SES
- **ReceiverEmailAddress:** Adresse email de la personne qui sera notifiée après le traitement - cette adresse email doit être créée et validée sur SES
- **SESIdentitySenderUser:** ARN de l'identité SES de SenderEmailAddress
- **TagKeysList:** Liste des clés des TAGS séparées par des virgules __ NB Le nombre de clés doit êre identique à celui de la variable TagValuesList. Exemple key1,key2
- **TagValuesList:** Liste des valeurs des TAGS séparées par des virgules __ NB -- Le nombre de valeurs doit êre identique à celui de la variable TagKeysList Exemple tag1,tag2

## Bonne pratique
Pour des raisons de sécurité, il n'est pas recommandé de stocker les données sensibles en clair dans vos fichiers de travails. 
Les données des variables **SenderEmailAddress**, **ReceiverEmailAddress** et **SESIdentitySenderUser** doivent être stokées 
sur SSM plus précisément sur **Parameter Store**. [Cliquez ici](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html)
pour apprendre à créer des entrées. 

###*Important*
Pour ce stack, nous utilisons des données de type *String* mais il est normalement d'autres possibilités. Il faut également
vous assurez de choisir l'option tier par défaut **Standard** pour ne pas être facturé.

## Comment déployer son stack
Nous verrons comment déployer son stack SAM à partir de Cloud9, l'IDE disponible sur AWS.
J'opte pour Cloud9 car il est *ready-to-go*. Il vient avec toutes les configurations nécessaires pour ce tutoriel 
et nous affranchit donc d'un travail supplémentaire.\
\
Vous pouvez également déployer le stack SAM en utilisant SAM CLI. [Cliquez ici](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) pour accéder à la documentation officielle. 
Le tutoriel suivant vous aidera à pendre la main rapidement : [Hello Worl Tutorial](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html).

### Les étapes à suivre
1. Créer un environnement Cloud9 en suivant le [lien](https://docs.aws.amazon.com/cloud9/latest/user-guide/tutorial-create-environment.html). Vérifier que vous utilisez une instance de type t2.micro pour profiter de l'offre free tiers 
2. Cloner le projet à l'aide de la commande `git clone https://github.com/isma237/StopEc2InstanceByTag.git`
3. Changer de repertoire: `cd StopEc2InstanceByTag`
4. Cliquer sur l'icône AWS dans la barre latérale gauche de Cloud9
5. Dans les options, faites un clic droit sur LAMBDA et choisir **Deploy SAM Application** et suiver le processus
   1. Choisir le template: Sélectionner `template.yaml`
   2. Vous serez ensuite invité à configurer les variables. Choisissez l'option *Configure*. Cloud9 générera un fichier contenant la liste des variables qui n'ont 
   aucune valeur par défaut. Vous pouvez vous servir de l'exemple ci-dessous pour configurer votre déploiement
   ```
   {
        "templates": {
            "template.yaml": {
                "parameterOverrides": {
                     "CronPlanification": "cron(30 19 * * *)",
                     "TagKeysList": "key1,key2",
                     "TagValuesList": "value1,value2"
                     "SenderEmailAddress": "/Dev/SenderEmailAddress"
                     "ReceiverEmailAddress": "/Dev/ReceiverAddress"
                     "SESIdentitySenderUser": "/Dev/SESIdentitySenderUser"
                }
            }
        }
   }
   ```
   3. Choisir le bucket S3 dans lequel les artefacts seront stockés
   4. Donner un nom au déploiement
   5. Suivre le processus de création et de déploiement depuis l'onglet AWS Toolkit
   

