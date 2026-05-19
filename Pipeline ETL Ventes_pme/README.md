# Pipeline ETL et dashboard d’analyse des ventes d’une PME

Projet data permettant de générer, stocker, analyser et visualiser des données de ventes à l’aide de Python, PostgreSQL, Docker et Streamlit.

## 1. Présentation du projet

### 1.1 À quoi sert le projet ?

Ce projet a pour objectif de simuler une chaîne complète de traitement et d’analyse de données de ventes pour une PME.

Dans un contexte d’entreprise, les données de ventes peuvent provenir de plusieurs magasins, concerner différents produits et être produites régulièrement. Pour être exploitables, ces données doivent être centralisées, structurées, analysées puis visualisées.

Ce projet répond à ce besoin en mettant en place un pipeline capable de générer des données de ventes, de les stocker dans une base PostgreSQL, d’exécuter des analyses SQL et d’afficher les résultats dans un dashboard web.

Il permet ainsi de transformer des données brutes en indicateurs utiles pour suivre l’activité commerciale d’une entreprise.

---

### 1.2 Fonctionnalités principales

Le projet intègre plusieurs fonctionnalités permettant de construire une chaîne complète de traitement des données.

- **Génération automatique des données** : le script `generate_data.py` crée des fichiers CSV simulant les produits, les magasins et les ventes d’une PME. Cela permet de tester le projet sans dépendre de données externes.

- **Import des données dans PostgreSQL** : les fichiers CSV sont lus par le script Python puis importés dans une base relationnelle. Les données sont ainsi centralisées et structurées.

- **Création automatique des tables** : le script crée les tables nécessaires au stockage des données, ce qui permet de lancer le projet plus facilement dans un nouvel environnement.

- **Gestion des doublons** : j’ai ajouté un mécanisme permettant d’éviter qu’une même vente soit importée plusieurs fois lorsque le pipeline est relancé. Cela permet de conserver des données fiables et d’éviter de fausser les résultats d’analyse.

- **Analyses SQL** : plusieurs requêtes permettent de calculer des indicateurs comme le chiffre d’affaires total, les ventes par produit, les ventes par ville ou encore l’évolution mensuelle du chiffre d’affaires.

- **Stockage des résultats** : les résultats des analyses sont enregistrés dans une table dédiée afin de conserver une trace des calculs effectués.

- **Dashboard Streamlit** : une interface web permet de visualiser les indicateurs et graphiques de manière plus lisible.


### 1.3 Fonctionnement du projet

Le projet fonctionne comme une chaîne de traitement automatisée.

Dans un premier temps, le script `generate_data.py` génère des fichiers CSV contenant les données nécessaires au projet : les produits, les magasins et les ventes.

Ensuite, le script `main.py` se connecte à PostgreSQL, crée les tables si elles n’existent pas encore, puis importe les données issues des fichiers CSV dans la base.

Une fois les données importées, le script exécute plusieurs requêtes SQL afin de calculer des indicateurs commerciaux. Les résultats sont ensuite stockés dans une table dédiée.

Enfin, le dashboard Streamlit se connecte à PostgreSQL pour récupérer les données et les afficher sous forme d’indicateurs et de graphiques.

Le fonctionnement global peut être résumé ainsi :

```text
generate_data.py
      ↓
fichiers CSV dans data/
      ↓
main.py
      ↓
base PostgreSQL ventes_pme
      ↓
analyses SQL
      ↓
dashboard Streamlit
 
```

### 1.4 Problèmes rencontrés et solutions apportées

Plusieurs problèmes techniques ont été rencontrés pendant la réalisation du projet.

Le projet avait d’abord été pensé avec SQLite, puis il a été adapté vers PostgreSQL afin d’utiliser une base de données plus adaptée à une architecture conteneurisée et plus proche d’un environnement professionnel.

Un autre problème concernait le démarrage des services Docker. Le script Python pouvait essayer de se connecter à PostgreSQL avant que la base soit complètement prête. Pour résoudre cela, un système de tentatives de connexion a été ajouté dans le script.

Des erreurs sont également apparues lors de l’import des fichiers CSV, notamment à cause de différences entre les colonnes des fichiers et celles des tables SQL. Les noms de colonnes et les requêtes d’insertion ont donc été adaptés pour assurer un import cohérent.

Enfin, une attention particulière a été portée à la gestion des doublons. Le pipeline peut être relancé plusieurs fois sans réimporter les mêmes ventes, ce qui permet de conserver des données fiables et des analyses correctes.

## 2. Analyse et valorisation des données

### 2.1 Analyses SQL réalisées

Une fois les données importées dans PostgreSQL, plusieurs analyses SQL sont exécutées afin d’extraire des indicateurs utiles à partir des ventes.

Ces analyses portent sur :

- le chiffre d’affaires total ;
- les ventes par produit ;
- les ventes par ville ;
- l’évolution du chiffre d’affaires par mois ;
- le top 5 des produits les plus performants ;
- le chiffre d’affaires par catégorie ;
- le chiffre d’affaires par salarié ;
- le stock restant théorique ;
- le nombre de ventes par mois ;
- le panier moyen par ville.

Ces requêtes permettent de transformer les données brutes en informations exploitables pour mieux comprendre l’activité commerciale de l’entreprise.

Les requêtes SQL sont regroupées dans le fichier `app/analyses.sql`.

### 2.2 Dashboard de visualisation

Un dashboard Streamlit a été ajouté afin de rendre les résultats plus accessibles et plus faciles à interpréter.

Il permet de consulter les principaux indicateurs sous forme de graphiques et de tableaux, sans avoir besoin d’exécuter directement les requêtes SQL dans la base de données.

Le dashboard est lancé dans un service Docker dédié et se connecte directement à la base PostgreSQL pour récupérer les données à afficher.

Une fois les services démarrés, il est consultable localement depuis un navigateur à l’adresse :

```text
http://localhost:8501
```

### 2.3 Utilisation possible en entreprise

Dans une entreprise, ce type d’analyse pourrait aider les équipes commerciales ou la direction à prendre des décisions plus éclairées.

Les indicateurs calculés permettent par exemple d’identifier les produits les plus rentables, de comparer les performances entre les villes, de suivre l’évolution du chiffre d’affaires dans le temps ou encore d’analyser les ventes par catégorie de produits.

Ces informations peuvent être utilisées pour ajuster les stocks, orienter les actions commerciales, repérer les magasins les plus performants ou identifier les produits à mettre davantage en avant.

Le projet montre ainsi comment des données brutes peuvent être transformées en informations utiles pour piloter l’activité commerciale d’une PME.

## 3. Technologies utilisées

- **Python** : utilisé pour générer les données, automatiser l’import des fichiers CSV, créer les tables et lancer les analyses.
- **Pandas** : utilisé pour lire et manipuler les fichiers CSV.
- **PostgreSQL** : utilisé comme base de données relationnelle pour stocker les produits, les magasins, les ventes et les résultats d’analyse.
- **SQL** : utilisé pour créer les tables, interroger les données et calculer les indicateurs commerciaux.
- **Psycopg2** : utilisé pour connecter les scripts Python à la base PostgreSQL.
- **Docker** : utilisé pour conteneuriser l’environnement du projet.
- **Docker Compose** : utilisé pour lancer et relier les différents services du projet : l’application Python, PostgreSQL et le dashboard.
- **Streamlit** : utilisé pour créer le dashboard web de visualisation des données.

## 4. Compétences développées

Ce projet m’a permis de développer des compétences liées à la mise en place d’un projet data complet, de la génération des données jusqu’à leur visualisation.

- **Pipeline ETL** : conception d’une chaîne de traitement permettant de générer, importer, analyser et stocker des données.
- **Modélisation de base de données** : création de tables relationnelles avec clés primaires, clés étrangères et relations entre les données.
- **SQL analytique** : écriture de requêtes SQL pour produire des indicateurs commerciaux exploitables.
- **PostgreSQL** : utilisation d’une base de données relationnelle dans un environnement Docker.
- **Docker et Docker Compose** : création d’une architecture avec plusieurs services connectés entre eux.
- **Traitement de données avec Python** : lecture de fichiers CSV, import en base et automatisation des traitements.
- **Visualisation de données** : création d’un dashboard Streamlit pour rendre les résultats plus lisibles.
- **Documentation de projet** : structuration et présentation du projet pour une mise en ligne sur GitHub.

## 5. Lancer le projet

Avant de lancer le projet, il faut avoir installé Docker et Docker Compose.

Commandes à exécuter dans l’ordre :


### 1. Réinitialiser les conteneurs et les volumes
```bash
docker compose down -v
```
### 2. Générer les fichiers CSV
```bash
docker compose run --rm --no-deps app python /app/generate_data.py
```
### 3. Lancer les services
```bash
docker compose up --build
```
### 4. Commandes utiles 

Lancer uniquement PostgreSQL et le dashboard
```bash
docker compose up -d db dashboard
```

Voir les conteneurs actifs
```bash
docker ps
```
