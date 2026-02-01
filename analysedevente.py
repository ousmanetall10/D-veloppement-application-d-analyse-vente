import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Dashboard KPI – DuckDB", layout="wide")
st.title(" Dashboard d’analyse des ventes ")

# --------------------------------------------------
# UPLOAD CSV
# --------------------------------------------------
uploaded_file = st.file_uploader(" Téléverser un fichier CSV", type=["csv"])

if uploaded_file is not None:

    # --------------------------------------------------
    # LECTURE
    # --------------------------------------------------
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower().str.strip()

    # --------------------------------------------------
    # DÉTECTION DU FICHIER
    # --------------------------------------------------
    is_amazon = "discounted_price" in df.columns
    is_bk = "attribute" in df.columns and "value" in df.columns
    is_mcd = "date" in df.columns and "value" in df.columns

    # --------------------------------------------------
    # NETTOYAGE SPÉCIFIQUE AMAZON
    # --------------------------------------------------
    if is_amazon:
        for col in ["discounted_price", "actual_price"]:
            if col in df.columns:
                df[col] = (
                    df[col].astype(str)
                    .str.replace("₹", "", regex=False)
                    .str.replace(",", "", regex=False)
                    .astype(float)
                )

        if "discount_percentage" in df.columns:
            df["discount_percentage"] = (
                df["discount_percentage"]
                .astype(str)
                .str.replace("%", "", regex=False)
                .astype(float)
            )

    # --------------------------------------------------
    # NETTOYAGE GÉNÉRAL (BK & MCD)
    # --------------------------------------------------
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = pd.to_numeric(df[col], errors="ignore")

    # --------------------------------------------------
    # DUCKDB
    # --------------------------------------------------
    con = duckdb.connect(database=":memory:")
    con.register("data", df)

    # --------------------------------------------------
    # SIDEBAR – FILTRE UNIQUE
    # --------------------------------------------------
    st.sidebar.header(" Filtre principal")

    if is_amazon:
        min_v, max_v = df["discounted_price"].min(), df["discounted_price"].max()
        slider = st.sidebar.slider(
            "Filtrer par discounted_price",
            float(min_v), float(max_v),
            (float(min_v), float(max_v))
        )
        df_f = df[
            (df["discounted_price"] >= slider[0]) &
            (df["discounted_price"] <= slider[1])
        ]
        value_col = "discounted_price"

    else:
        min_v, max_v = df["value"].min(), df["value"].max()
        slider = st.sidebar.slider(
            "Filtrer par Value",
            float(min_v), float(max_v),
            (float(min_v), float(max_v))
        )
        df_f = df[
            (df["value"] >= slider[0]) &
            (df["value"] <= slider[1])
        ]
        value_col = "value"

    con.unregister("data")
    con.register("data", df_f)

    # --------------------------------------------------
    # KPI
    # --------------------------------------------------
    st.subheader(" Indicateurs clés de performance (KPI)")

    c1, c2, c3, c4 = st.columns(4)

    kpi1 = con.execute("SELECT COUNT(*) FROM data").fetchone()[0]
    kpi2 = con.execute(f"SELECT AVG({value_col}) FROM data").fetchone()[0]
    kpi3 = con.execute(f"SELECT MIN({value_col}) FROM data").fetchone()[0]
    kpi4 = con.execute(f"SELECT MAX({value_col}) FROM data").fetchone()[0]

    c1.metric("Nb ventes", kpi1)
    c2.metric("Moyenne", round(kpi2, 2))
    c3.metric("Min", round(kpi3, 2))
    c4.metric("Max", round(kpi4, 2))

    # --------------------------------------------------
    # VISUALISATIONS – 1 PAR KPI
    # --------------------------------------------------
    st.subheader(" Visualisation des KPI (compact)")

    v1, v2 = st.columns(2)
    v3, v4 = st.columns(2)

    # KPI 1 – Histogramme
    with v1:
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.hist(df_f[value_col], color="#69b3a2", edgecolor="black")
        ax.set_title("Distribution des ventes", fontsize=10)
        ax.tick_params(axis='both', labelsize=8)
        st.pyplot(fig)

    # KPI 2 – Boxplot
    with v2:
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.boxplot(df_f[value_col])
        ax.set_title("Dispersion des valeurs", fontsize=10)
        ax.tick_params(axis='both', labelsize=8)
        st.pyplot(fig)

    # KPI 3 – Courbe cumulative
    with v3:
        fig, ax = plt.subplots(figsize=(3, 2))
        df_f[value_col].sort_values().cumsum().plot(ax=ax, color="#ff7f0e")
        ax.set_title("Évolution cumulée", fontsize=10)
        ax.tick_params(axis='both', labelsize=8)
        st.pyplot(fig)

    # KPI 4 – Camembert
    with v4:
        fig, ax = plt.subplots(figsize=(3, 2))  # carré pour bien voir le camembert

        if is_amazon and "product_name" in df_f.columns:
            df_f["product_name"].value_counts().head(5).plot(
                kind="pie", autopct="%1.1f%%", ax=ax, textprops={'fontsize':8}
            )
            ax.set_title("Répartition par produit", fontsize=10)

        elif is_bk:
            df_f["attribute"].value_counts().plot(
                kind="pie", autopct="%1.1f%%", ax=ax, textprops={'fontsize':8}
            )
            ax.set_title("Répartition par attribut", fontsize=10)

        elif is_mcd and "item" in df_f.columns:
            df_f["item"].value_counts().head(5).plot(
                kind="pie", autopct="%1.1f%%", ax=ax, textprops={'fontsize':8}
            )
            ax.set_title("Répartition par item", fontsize=10)

        st.pyplot(fig)

    # --------------------------------------------------
    # APERÇU FINAL
    # --------------------------------------------------
    st.subheader(" Filtrer dynamiquement les résultats par date, région ou produit")
    st.dataframe(df_f.head(6), use_container_width=True)






