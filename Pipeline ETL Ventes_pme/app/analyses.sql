-- 1. Chiffre d'affaires total
SELECT 
    ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires_total
FROM ventes v
JOIN produits p 
    ON v.id_reference_produit = p.id_reference_produit;


-- 2. Ventes par produit
SELECT 
    p.nom AS produit,
    SUM(v.quantite) AS quantite_totale_vendue,
    ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
FROM ventes v
JOIN produits p 
    ON v.id_reference_produit = p.id_reference_produit
GROUP BY p.nom
ORDER BY chiffre_affaires DESC;


-- 3. Ventes par ville
SELECT 
    m.ville,
    SUM(v.quantite) AS quantite_totale_vendue,
    ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
FROM ventes v
JOIN produits p 
    ON v.id_reference_produit = p.id_reference_produit
JOIN magasins m 
    ON v.id_magasin = m.id_magasin
GROUP BY m.ville
ORDER BY chiffre_affaires DESC;


-- 4. Chiffre d'affaires par mois
SELECT
    TO_CHAR(DATE_TRUNC('month', v.date_vente), 'YYYY-MM') AS mois,
    ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
FROM ventes v
JOIN produits p
    ON v.id_reference_produit = p.id_reference_produit
GROUP BY DATE_TRUNC('month', v.date_vente)
ORDER BY mois;


-- 5. Top 5 des produits par chiffre d'affaires
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


-- 6. Chiffre d'affaires par catégorie
SELECT
    p.categorie,
    SUM(v.quantite) AS quantite_vendue,
    ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires
FROM ventes v
JOIN produits p
    ON v.id_reference_produit = p.id_reference_produit
GROUP BY p.categorie
ORDER BY chiffre_affaires DESC;


-- 7. Chiffre d'affaires par salarié
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


-- 8. Stock restant théorique
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


-- 9. Nombre de ventes par mois
SELECT
    TO_CHAR(DATE_TRUNC('month', date_vente), 'YYYY-MM') AS mois,
    COUNT(*) AS nombre_ventes
FROM ventes
GROUP BY DATE_TRUNC('month', date_vente)
ORDER BY mois;


-- 10. Panier moyen par ville
SELECT
    m.ville,
    COUNT(v.id_vente) AS nombre_ventes,
    ROUND(SUM(v.quantite * p.prix), 2) AS chiffre_affaires,
    ROUND(SUM(v.quantite * p.prix) / COUNT(v.id_vente), 2) AS panier_moyen
FROM ventes v
JOIN magasins m
    ON v.id_magasin = m.id_magasin
JOIN produits p
    ON v.id_reference_produit = p.id_reference_produit
GROUP BY m.ville
ORDER BY panier_moyen DESC;