
# Digitruc: StopEc2InstancesByTagsDefinition

### Pourquoi ?
Est-ce qu'il vous arrive aussi d'oublier d'éteindre vos instances 
EC2 après avoir réalisé des labs sur AWS ?

Si comme moi, il vous arrive d'oublier d'arrêter d'éteindre 
vos instances EC2 après avoir terminés des labs,  alors ce projet pourrait vous interesser. 

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
2. Configurer AWS CLI: Suivre le tutoriel suivant [Configurer AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
3. Installer Git sur votre environnement Cloud9. Vous pouvez suivre le tutoriel suivant [Installer Git](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-centos-7)
4. Clôner le projet à l'aide de la commande `git clone https://github.com/isma237/StopEc2InstanceByTag.git`
5. Changer de repertoire: `cd StopEc2InstanceByTag`
6. Cliquer sur l'icône AWS dans la barre latérale gauche de  cloud9
7. Dans les options, faites un clique droit sur LAMBDA et choisir **Deploy SAM Application** et suiver le processus
   1. Choisir le template: Sélectionner `template.yaml`
   2. Accepter de configurer les variables. Cloud9  générera un fichier contenant la liste des variables qui n'ont 
   aucune valeur par défault. Vous pouvez vous servir de l'exemple ci-dessous pour configurer votre déploiement
   ```
   {
        "templates": {
            "template.yaml": {
                "parameterOverrides": {
                     "CronPlanification": "cron(30 19 * * *)",
                     "TagKeysList": "key1,key2",
                     "TagValuesList": "value1,value2",
                     "EventBridgeDescription": "Sample Description",
                     "EventBridgeName": "CallerStopEC2Instances"
                }
            }
        }
   }
   ```
   3. Choisir le bucket S3 dans lequel les artefacts seront stockés
   4. Suivre le processus de création et de déploiement depuis l'onglet AWS Toolkit
   

