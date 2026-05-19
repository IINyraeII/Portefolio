import time
import psycopg2
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Dashboard ventes PME",
    layout="wide"
)


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
            st.warning("Connexion à PostgreSQL en attente...")
            time.sleep(2)

    st.error("Impossible de se connecter à PostgreSQL.")
    st.stop()


def charger_donnees(requete):
    conn = connecter_db()
    df = pd.read_sql_query(requete, conn)
    conn.close()
    return df


st.title("Dashboard des ventes PME")

st.write(
    "Ce dashboard présente les principaux indicateurs de ventes "
    "à partir des données stockées dans PostgreSQL."
)


ca_total = charger_donnees("""
    SELECT ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires_total
    FROM ventes v
    JOIN produits p
        ON v.id_reference_produit = p.id_reference_produit;
""")

nb_ventes = charger_donnees("""
    SELECT COUNT(*) AS nombre_ventes
    FROM ventes;
""")

nb_produits = charger_donnees("""
    SELECT COUNT(*) AS nombre_produits
    FROM produits;
""")

nb_magasins = charger_donnees("""
    SELECT COUNT(*) AS nombre_magasins
    FROM magasins;
""")


col1, col2, col3, col4 = st.columns(4)

col1.metric("Chiffre d'affaires total", f"{ca_total.iloc[0, 0]:,.2f} €")
col2.metric("Nombre de ventes", int(nb_ventes.iloc[0, 0]))
col3.metric("Nombre de produits", int(nb_produits.iloc[0, 0]))
col4.metric("Nombre de magasins", int(nb_magasins.iloc[0, 0]))



st.subheader("Chiffre d'affaires par mois")

ca_mois = charger_donnees("""
    SELECT
        TO_CHAR(DATE_TRUNC('month', v.date_vente), 'YYYY-MM') AS mois,
        ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
    FROM ventes v
    JOIN produits p
        ON v.id_reference_produit = p.id_reference_produit
    GROUP BY DATE_TRUNC('month', v.date_vente)
    ORDER BY mois;
""")

st.line_chart(ca_mois.set_index("mois"))


st.subheader("Top 5 des produits par chiffre d'affaires")

top_produits = charger_donnees("""
    SELECT 
        p.nom AS produit,
        ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
    FROM ventes v
    JOIN produits p
        ON v.id_reference_produit = p.id_reference_produit
    GROUP BY p.nom
    ORDER BY chiffre_affaires DESC
    LIMIT 5;
""")

st.bar_chart(top_produits.set_index("produit"))


st.subheader("Chiffre d'affaires par ville")

ca_ville = charger_donnees("""
    SELECT 
        m.ville,
        ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
    FROM ventes v
    JOIN produits p 
        ON v.id_reference_produit = p.id_reference_produit
    JOIN magasins m 
        ON v.id_magasin = m.id_magasin
    GROUP BY m.ville
    ORDER BY chiffre_affaires DESC;
""")

st.bar_chart(ca_ville.set_index("ville"))


st.subheader("Chiffre d'affaires par catégorie")

ca_categorie = charger_donnees("""
    SELECT
        p.categorie,
        ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
    FROM ventes v
    JOIN produits p
        ON v.id_reference_produit = p.id_reference_produit
    GROUP BY p.categorie
    ORDER BY chiffre_affaires DESC;
""")

st.bar_chart(ca_categorie.set_index("categorie"))


st.subheader("Données détaillées")

onglet1, onglet2, onglet3 = st.tabs([
    "Top produits",
    "Villes",
    "Catégories"
])

with onglet1:
    st.dataframe(top_produits)

with onglet2:
    st.dataframe(ca_ville)

with onglet3:
    st.dataframe(ca_categorie)