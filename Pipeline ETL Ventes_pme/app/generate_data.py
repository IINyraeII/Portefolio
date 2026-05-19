# -*- coding: utf-8 -*-

import random
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd


DATA_DIR = Path("/data")

PRODUITS_CSV = DATA_DIR / "produits.csv"
MAGASINS_CSV = DATA_DIR / "magasins.csv"
VENTES_CSV = DATA_DIR / "ventes.csv"


def generer_produits(nombre_produits=50):
    categories = [
        "Informatique",
        "Bureautique",
        "Accessoires",
        "Reseau",
        "Stockage"
    ]

    produits = []

    for i in range(1, nombre_produits + 1):
        reference = f"REF{i:03d}"
        categorie = random.choice(categories)

        produits.append({
            "Nom": f"Produit {i}",
            "ID Référence produit": reference,
            "Prix": round(random.uniform(9.99, 499.99), 2),
            "Stock": random.randint(20, 500),
            "Categorie": categorie
        })

    return pd.DataFrame(produits)


def generer_magasins(nombre_magasins=20):
    villes = [
        "Paris", "Lyon", "Marseille", "Bordeaux", "Nantes",
        "Lille", "Strasbourg", "Toulouse", "Nice", "Rennes",
        "Grenoble", "Dijon", "Montpellier", "Reims", "Angers",
        "Tours", "Clermont-Ferrand", "Metz", "Rouen", "Annecy"
    ]

    magasins = []

    for i in range(1, nombre_magasins + 1):
        magasins.append({
            "ID Magasin": i,
            "Ville": villes[i - 1],
            "Nombre de salariés": random.randint(3, 30)
        })

    return pd.DataFrame(magasins)


def generer_ventes(produits, magasins, nombre_ventes=10000):
    ventes = []

    date_debut = datetime.now() - timedelta(days=365)

    references_produits = produits["ID Référence produit"].tolist()
    ids_magasins = magasins["ID Magasin"].tolist()

    for _ in range(nombre_ventes):
        date_vente = date_debut + timedelta(days=random.randint(0, 365))

        ventes.append({
            "Date": date_vente.strftime("%Y-%m-%d"),
            "ID Référence produit": random.choice(references_produits),
            "Quantité": random.randint(1, 10),
            "ID Magasin": random.choice(ids_magasins)
        })

    return pd.DataFrame(ventes)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    produits = generer_produits(nombre_produits=50)
    magasins = generer_magasins(nombre_magasins=20)
    ventes = generer_ventes(produits, magasins, nombre_ventes=10000)

    produits.to_csv(PRODUITS_CSV, index=False, encoding="utf-8")
    magasins.to_csv(MAGASINS_CSV, index=False, encoding="utf-8")
    ventes.to_csv(VENTES_CSV, index=False, encoding="utf-8")

    print("Fichiers generes avec succes :")
    print(f"- {PRODUITS_CSV} : {len(produits)} produits")
    print(f"- {MAGASINS_CSV} : {len(magasins)} magasins")
    print(f"- {VENTES_CSV} : {len(ventes)} ventes")


if __name__ == "__main__":
    main()