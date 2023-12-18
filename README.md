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

## execution du code
Le projet est dockerisé, on utilise docker-compose.
Si on veut l'environement dev on fait
```
docker-compose build
docker-compose up web
```

Si on veut lancer les tests:
```
docker-compose build
docker-compose up test
```


## Qu’est-ce que tu aurais fait pour améliorer ton test si tu avais eu plus de temps?
plusieurs fonctionnalités manquantes que j'ai pas eu l'occasion de faire au 18/12 matin  
=> auth service  
=> +++ de conditions sur les champs des classes (pas de % de réduction >= 100 par exemple)  
=> simplifier le mapping de la météo y'a des champs ridicules (tornade :joy:) et on pourrait tout mapper sur météo claire/pluie  
=> les tests tels qu'ils sont génèrent du coverage et des cas d'utilisation simples, mais il faut tester des comportements d'utilisateur et de vendeurs mais ca demanderai + de contexte.  
=> si je rentre une ville comme lyon en entrée de mon /apply_promocode j'ai a priori pas de soucis mais si je rentre Saint-Martin (255 communes) je vais avoir des problèmes.  
=> si je devais repasser du temps je refactoriserai un peu mon code pour rendre certaines fonctions moins longues et pouvoir tester des bouts de fonctions unitairement.  