# Pipeline ETL et dashboard d’analyse des ventes d’une PME

## Présentation

Ce projet met en place un pipeline de traitement et d’analyse de données de ventes pour une PME.

Il permet de générer des données de ventes, de les importer dans une base PostgreSQL, d’exécuter des analyses SQL, puis de visualiser les résultats dans un dashboard web Streamlit.

L’ensemble du projet est conteneurisé avec Docker Compose afin de faciliter son lancement et sa reproductibilité.

---

## Objectifs du projet

L’objectif est de construire une chaîne data complète permettant de :

- générer automatiquement des données de ventes au format CSV ;
- stocker les données dans une base PostgreSQL ;
- structurer les données dans plusieurs tables relationnelles ;
- éviter l’import de ventes en doublon ;
- exécuter des analyses SQL ;
- stocker les résultats des analyses ;
- afficher les indicateurs clés dans un dashboard.

---

## Technologies utilisées

- Python
- PostgreSQL
- SQL
- Docker
- Docker Compose
- Pandas
- Psycopg2
- Streamlit

---

## Architecture

Le projet repose sur trois services Docker principaux :

| Service | Rôle |
|---|---|
| App Python ETL | Génère les données, crée les tables, importe les CSV, exécute les analyses SQL |
| PostgreSQL | Stocke les données du projet dans une base relationnelle |
| Dashboard Streamlit | Affiche les indicateurs et graphiques depuis PostgreSQL |

La base de données PostgreSQL est conservée dans un volume Docker nommé `postgres_data`.

Un dossier `data/` est utilisé comme espace temporaire pour les fichiers CSV générés.

---

## Structure du projet

```text
projet_ventes_pme/
├── app/
│   ├── main.py
│   ├── generate_data.py
│   ├── analyses.sql
│   └── requirements.txt
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│   └── .gitkeep
│
├── docs/
│   ├── architecture.png
│   └── schema_donnees.png
│
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
