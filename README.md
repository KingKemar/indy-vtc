# indy-vtc

Test technique Indy

service de gestion de *promocodes* où :

- l'équipe Marketing pourra ajouter des *promocodes* dont la validité dépendra d'un ou plusieurs critères
- et l'application pourra vérifier la validité d'un *promocode* et obtenir la réduction associée.

## Configuration
Pour configurer correctement l'environnement de l'application, vous devez créer deux fichiers de variables d'environnement : .env pour le développement et .env.test pour les tests.

Créez un fichier nommé .env et .env.test à la racine du projet avec le contenu suivant :
```
MONGO_INITDB_ROOT_USERNAME=<nom_utilisateur_mongo>
MONGO_INITDB_ROOT_PASSWORD=<mot_de_passe_mongo>
MONGO_DB_NAME=<nom_de_la_base_de_donnees>
MONGO_USER=<nom_utilisateur_mongo>
MONGO_PASSWORD=<mot_de_passe_mongo>
FLASK_APP_ENV=development
METEO_API_KEY=<votre_cle_api_meteo>
HOST=mongodb
```
Remplacez les valeurs entre < > par vos propres configurations.


