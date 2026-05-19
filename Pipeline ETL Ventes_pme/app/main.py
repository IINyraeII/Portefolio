# -*- coding: utf-8 -*-
import time
import psycopg2
from pathlib import Path
import pandas as pd
import requests

PRODUITS_CSV = "/data/produits.csv"
MAGASINS_CSV = "/data/magasins.csv"
VENTES_CSV = "/data/ventes.csv"

URL_PRODUITS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
URL_MAGASINS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
URL_VENTES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"

def connecter_db():
    for tentative in range(10):
        try:
            return psycopg2.connect(
                host="db",
                database="ventes_pme",
                user="postgres",
                password="postgres"
            )
        except psycopg2.OperationalError:
            print("PostgreSQL pas encore pret, nouvelle tentative...")
            time.sleep(2)

    raise Exception("Impossible de se connecter a PostgreSQL apres plusieurs tentatives.")

        
def executer_analyses():
    conn = connecter_db()
    cursor = conn.cursor()

    # On vide les anciens resultats pour eviter les doublons
    cursor.execute("DELETE FROM resultats_analyses;")

    requetes = {
        "chiffre_affaires_par_mois": """
            SELECT
                TO_CHAR(DATE_TRUNC('month', v.date_vente), 'YYYY-MM') AS mois,
                ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
            FROM ventes v
            JOIN produits p
                ON v.id_reference_produit = p.id_reference_produit
            GROUP BY DATE_TRUNC('month', v.date_vente)
            ORDER BY mois;
        """,

        "top_5_produits": """
            SELECT 
                p.nom AS produit,
                SUM(v.quantite) AS quantite_vendue,
                ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
            FROM ventes v
            JOIN produits p
                ON v.id_reference_produit = p.id_reference_produit
            GROUP BY p.nom
            ORDER BY chiffre_affaires DESC
            LIMIT 5;
        """,

        "chiffre_affaires_par_categorie": """
            SELECT
                p.categorie,
                SUM(v.quantite) AS quantite_vendue,
                ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
            FROM ventes v
            JOIN produits p
                ON v.id_reference_produit = p.id_reference_produit
             GROUP BY p.categorie
            ORDER BY chiffre_affaires DESC;
        """,
        "chiffre_affaires_par_salarie": """
            SELECT
                m.ville,
                m.nombre_salaries,
                ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires,
                ROUND(SUM(v.quantite * p.prix) / m.nombre_salaries, 2) AS ca_par_salarie
            FROM ventes v
            JOIN magasins m
                ON v.id_magasin = m.id_magasin
            JOIN produits p
                ON v.id_reference_produit = p.id_reference_produit
            GROUP BY m.ville, m.nombre_salaries
            ORDER BY ca_par_salarie DESC;
        """,
        "stock_restant_theorique": """
            SELECT
             p.nom AS produit,
                p.stock AS stock_initial,
                COALESCE(SUM(v.quantite), 0) AS quantite_vendue,
                p.stock - COALESCE(SUM(v.quantite), 0) AS stock_restant_theorique
            FROM produits p
            LEFT JOIN ventes v
                ON p.id_reference_produit = v.id_reference_produit
            GROUP BY p.id_reference_produit, p.nom, p.stock
            ORDER BY stock_restant_theorique ASC;
        """
    }

    for nom_analyse, requete in requetes.items():
        resultat = pd.read_sql_query(requete, conn)

        print("")
        print("Analyse :", nom_analyse)
        print(resultat)

        cursor.execute(
            """
            INSERT INTO resultats_analyses (nom_analyse, resultat)
            VALUES (%s, %s)
            """,
            (nom_analyse, resultat.to_json(orient="records", force_ascii=False))
        )

    conn.commit()
    cursor.close()
    conn.close()

    print("Resultats des analyses stockes avec succes.")

def lire_csv(chemin):
    try:
        return pd.read_csv(chemin, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(chemin, encoding="latin1")


def creer_tables():
    conn = connecter_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits (
        id_reference_produit TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        prix NUMERIC(10, 2) NOT NULL,
        stock INTEGER,
        categorie TEXT           
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS magasins (
        id_magasin INTEGER PRIMARY KEY,
        ville TEXT NOT NULL,
        nombre_salaries INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventes (
        id_vente SERIAL PRIMARY KEY,
        date_vente DATE,
        id_reference_produit TEXT,
        quantite INTEGER,
        id_magasin INTEGER,
        UNIQUE(date_vente, id_reference_produit, quantite, id_magasin),
        FOREIGN KEY (id_reference_produit) REFERENCES produits(id_reference_produit),
        FOREIGN KEY (id_magasin) REFERENCES magasins(id_magasin)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultats_analyses (
        id_resultat SERIAL PRIMARY KEY,
        nom_analyse TEXT NOT NULL,
        resultat TEXT NOT NULL,
        date_calcul TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Tables creees avec succes.")



def importer_donnees():
    conn = connecter_db()

    produits = lire_csv(PRODUITS_CSV)
    magasins = lire_csv(MAGASINS_CSV)
    ventes = lire_csv(VENTES_CSV)

    print("Colonnes produits :", list(produits.columns))
    print("Colonnes magasins :", list(magasins.columns))
    print("Colonnes ventes :", list(ventes.columns))

    produits = produits.rename(columns={
        produits.columns[0]: "nom",
        produits.columns[1]: "id_reference_produit",
        produits.columns[2]: "prix",
        produits.columns[3]: "stock",
        produits.columns[4]: "categorie"
    })

    magasins = magasins.rename(columns={
        magasins.columns[0]: "id_magasin",
        magasins.columns[1]: "ville",
        magasins.columns[2]: "nombre_salaries"
    })

    ventes = ventes.rename(columns={
        ventes.columns[0]: "date_vente",
        ventes.columns[1]: "id_reference_produit",
        ventes.columns[2]: "quantite",
        ventes.columns[3]: "id_magasin"
    })

    cursor = conn.cursor()

    for _, row in produits.iterrows():
        cursor.execute("""
            INSERT INTO produits (nom, id_reference_produit, prix, stock,categorie)
            VALUES (%s, %s, %s, %s,%s)
            ON CONFLICT (id_reference_produit)
            DO UPDATE SET
                nom = EXCLUDED.nom,
                prix = EXCLUDED.prix,
                stock = EXCLUDED.stock,
                categorie = EXCLUDED.categorie;
        """, (
            row["nom"],
            row["id_reference_produit"],
            row["prix"],
            row["stock"],
            row["categorie"]
        ))

    for _, row in magasins.iterrows():
        cursor.execute("""
            INSERT INTO magasins (id_magasin, ville, nombre_salaries)
            VALUES (%s, %s, %s)
            ON CONFLICT (id_magasin)
            DO UPDATE SET
                ville = EXCLUDED.ville,
                nombre_salaries = EXCLUDED.nombre_salaries;
        """, (
            row["id_magasin"],
            row["ville"],
            row["nombre_salaries"]
        ))

    nouvelles_ventes = 0

    for _, row in ventes.iterrows():
        cursor.execute("""
            INSERT INTO ventes (
                date_vente,
                id_reference_produit,
                quantite,
                id_magasin
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (date_vente, id_reference_produit, quantite, id_magasin)
            DO NOTHING;
        """, (
            row["date_vente"],
            row["id_reference_produit"],
            row["quantite"],
            row["id_magasin"]
        ))

        if cursor.rowcount == 1:
            nouvelles_ventes += 1

    conn.commit()
    cursor.close()
    conn.close()

    print("Produits importes :", len(produits))
    print("Magasins importes :", len(magasins))
    print("Nouvelles ventes importees :", nouvelles_ventes)


creer_tables()
importer_donnees()
executer_analyses()