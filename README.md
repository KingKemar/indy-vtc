# Test technique Indy

## **Contexte**

Tu fais partie d'une entreprise de réservation de VTC (de type Uber) et l'équipe Marketing souhaite encourager les clients à réserver un trajet en leur proposant des promotions.

Pour cela, elle souhaite s'équiper d'un service de gestion de *promocodes* où :

- l'équipe Marketing pourra ajouter des *promocodes* dont la validité dépendra d'un ou plusieurs critères
- et l'application pourra vérifier la validité d'un *promocode* et obtenir la réduction associée.

L'objectif de ce test est de construire ce service avec son API. Tu pourras t'aider de n'importe quel framework, librairie ou outil que tu jugeras utiles.

## **Spécifications**

### **Structure d'un** *promocode*

Tout promocode se compose d'un nom, d'un avantage (la réduction associée) et d'une ou plusieurs restrictions (les critères de validité du promocode).

Pour qu'un promocode soit validé, il faut que toutes ses restrictions soient validées.

Les restrictions sont définies par différentes règles intitulées `@age`, `@date`, `@meteo`, `@or` et `@and`. Les règles `@or` et `@and` incluent d'autres règles.

> Une règle `@or` ou `@and` pouvant inclure d'autres règles `@or` ou `@and`, **l'arbre des restrictions peut aller jusqu'à une profondeur arbitraire**.
> 

Voici un exemple de promocode :

```json
{
  "_id": "...",
  "name": "WeatherCode",
  "avantage": { "percent": 20 },
  "restrictions": [
    {
      "@date": {
        "after": "2019-01-01",
        "before": "2020-06-30"
      }
    },
    {
      "@or": [
        {
          "@age": {
            "eq": 40
          }
        },
        {
          "@and": [
            {
              "@age": {
                "lt": 30,
                "gt": 15
              }
            },
            {
              "@meteo": {
                "is": "clear",
                "temp": {
                  "gt": "15" // Celsius here.
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

Ce promocode se lit de la manière suivante :

- Il peut être utilisé si la date d'aujourd'hui est comprise entre le 1er janvier 2019 et le 30 juin 2020.
- Il faut que le client ait soit 40 ans ou soit qu'il ait entre 15 et 30 ans et que la température extérieure soit supérieure à 15 °C avec un soleil radieux.
- Si le client valide ces restrictions, alors il obtient une réduction de 20 % sur son trajet.

### **Ajout d'un** *promocode*

👉 **Consigne : le service doit exposer une route pour pouvoir ajouter et sauvegarder des promocodes.**

> Pour la sauvegarde des données, il n'est pas nécessaire d'utiliser une vraie base de données. Une implémentation basique en mémoire est amplement suffisante.
> 

### **Validation d'un** *promocode* **et obtention de la réduction**

👉 **Consigne : le service doit exposer une deuxième route pour valider l'utilisation d'un promocode et obtenir la réduction associée pour un utilisateur donné.**

*Exemple de requête :*

```json
{
  "promocode_name": "WeatherCode",
  "arguments": {
    "age": 25,
    "meteo": { "town": "Lyon" }
  }
}
```

*Exemple de réponse si le promocode est validé :*

```json
{
  "promocode_name": "WeatherCode",
  "status": "accepted",
  "avantage": { "percent": 20 }
}
```

*Exemple de réponse si le promocode est invalidé :*

```json
{
  "promocode_name": "WeatherCode",
  "status": "denied",
  "reasons": {
    // Les raisons pour lesquelles le promocode n'a pas été validé
  }
}
```

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
