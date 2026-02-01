# D-veloppement-application-d-analyse-vente

# Dashboard KPI – Streamlit & DuckDB

## Description
Application web interactive développée avec Streamlit permettant
d’analyser des données de ventes à partir de fichiers CSV.
Les données sont stockées et interrogées via DuckDB, une base de données
analytique embarquée, offrant des requêtes SQL rapides et efficaces sans
dépendre d’un serveur externe.

L’application permet tout d’abord de filtrer les données pour ne regarder que ce qui nous intéresse, par exemple uniquement les ventes d’Amazon dont le prix est compris entre 100 et 500 ₹, ou les ventes d’un produit spécifique. Une fois les données sélectionnées, elle analyse les données brutes et les transforme en informations utiles en calculant automatiquement des chiffres clés (KPI) qui résument les performances : le nombre total de ventes réalisées, la valeur moyenne d’une vente, ainsi que la valeur minimale et maximale des ventes. Enfin, pour comprendre rapidement ces informations, l’application affiche des graphiques distincts pour chaque KPI : un histogramme pour visualiser la répartition des ventes, un boxplot pour identifier les ventes extrêmes, une courbe cumulative pour observer l’accumulation des ventes dans le temps ou par valeur, et un camembert pour montrer la part de chaque produit ou catégorie dans le total des ventes. Ces représentations permettent de tirer des conclusions simples et immédiates sur les tendances et la répartition des ventes.

## Fonctionnalités

Téléversement de fichiers CSV


Stockage des données dans DuckDB (en mémoire)


Calcul de 4 indicateurs clés de performance (KPI) :

Nombre de ventes
Valeur moyenne
Valeur minimale
Valeur maximale


Visualisation de chaque KPI via un graphique distinct :

Histogramme
Boxplot
Courbe cumulative
Diagramme circulaire (camembert)


Filtres dynamiques via curseur (adapté au fichier chargé)

Mise à jour automatique des KPI et des visualisations
Interface web interactive sur une seule page



## Technologies utilisées
- Python 3.11
- Streamlit
- DuckDB
- Pandas
- Matplotlib


## Lancer l’application

pip install -r requirements.txt  qui sert à installer automatiquement toutes les bibliothèques nécessaires au projet, en une seule fois.
streamlit run analysedevente.py

streamlit run app.py

