from utils.data import get_teams_data, get_players_data, get_matches_data
from utils.const import RC, GRAPHIC_PATH

import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

import altair as alt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from typing import Dict

TEAMS = [
    "Atalanta",
    "Bologna",
    "Cremonese",
    "Empoli",
    "Fiorentina",
    "Inter",
    "Juventus",
    "Lazio",
    "Lecce",
    "AC Milan",
    "Monza",
    "Napoli",
    "Roma",
    "Salernitana",
    "Sampdoria",
    "Sassuolo",
    "Spezia",
    "Torino",
    "Udinese",
    "Verona",
]


def main():
    plt.rcParams.update(RC)

    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    high_icon = Image.open(GRAPHIC_PATH / "nome_logo_orizzontale.png")
    st.set_page_config(page_icon=icon, page_title="SIGMASUITE", layout="wide")

    cols = st.columns((0.8, 0.2))
    with cols[1]:
        st.image(high_icon, use_column_width=True)
    with cols[0]:
        st.title("Tabellone statistico")

    players_data = get_players_data(separate_multi_team_players=False)
    players_data.index = players_data.player_name
    players_data.drop(columns=["player_name"], inplace=True)

    min_time = st.slider(
        label="Minimo minuti giocati",
        min_value=0,
        max_value=1500,
        value=90,
    )

    players_data = players_data[players_data.time >= min_time]

    st.dataframe(players_data.style.format(precision=2))

    players_data["npg/npxG"] = players_data.npg / players_data.npxG

    players_data["Rigori calciati"] = (
        (players_data.xG - (players_data.npxG)) / 0.76
    ).astype("int")
    players_data["npShots"] = players_data.shots - players_data["Rigori calciati"]

    players_data["npxG/npShots"] = players_data.npxG / players_data.npShots

    players_data["npShots/90"] = players_data.npShots / players_data.time * 90

    players_data["npxG/90"] = players_data.npxG / players_data.time * 90
    players_data["npg/90"] = players_data.npg / players_data.time * 90

    players_data["KP/90"] = players_data.key_passes / players_data.time * 90
    players_data["xA/90"] = players_data.xA / players_data.time * 90
    players_data["assists/90"] = players_data.assists / players_data.time * 90
    players_data["xA/KP"] = players_data.xA / players_data.key_passes
    players_data["assists/KP"] = players_data.assists / players_data.key_passes

    players_data["yellow_cards/90"] = players_data.yellow_cards / players_data.time * 90
    players_data["red_cards/90"] = players_data.red_cards / players_data.time * 90

    st.header("Goal")

    fin_data = players_data[players_data.npShots > 0][
        [
            "npShots/90",
            "npxG/npShots",
            "npxG/90",
            "npg/90",
            "npg/npxG",
            "Rigori calciati",
        ]
    ]

    st.dataframe(fin_data.style.format(precision=2))

    st.header("Assist")

    as_data = players_data[players_data.key_passes > 0][
        ["KP/90", "xA/90", "assists/90", "xA/KP", "assists/KP"]
    ]

    st.dataframe(as_data.style.format(precision=2))

    st.header("Cartellini")

    card_data = players_data[
        [
            "yellow_cards/90",
            "red_cards/90",
        ]
    ]

    st.dataframe(card_data.style.format(precision=2))

    st.write(
        "Le statistiche /90 minuti possono essere leggerment imprecise, in quanto ottenute dividendo per il numero di partite giocate, non di minuti giocati"
    )

    st.header("PCA analysis")
    stat_at_columns = [
        "shots",
        "xA",
        "key_passes",
        "npxG",
        "xGChain",
        "xGBuildup",
    ]
    stat_def_columns = ["red_cards", "yellow_cards"]

    stat_data = players_data[stat_def_columns + stat_at_columns]

    pca = PCA(n_components=2)
    scaler = StandardScaler()
    scaled_data = pd.DataFrame(
        scaler.fit_transform(stat_data), columns=stat_data.columns
    )
    pca_data = pd.DataFrame(pca.fit_transform(scaled_data), columns=["PC1", "PC2"])

    print(type(pca_data))
    pca_data["team"] = players_data.index

    st.write(
        "PCA explained variance: "
        + str(round(sum(pca.explained_variance_ratio_) * 100, 2))
        + "%"
    )

    scatter_plot = (
        alt.Chart(pca_data).mark_point(size=100).encode(x="PC1:Q", y="PC2:Q")
    ).properties(width=1200, height=700)

    text = scatter_plot.mark_text(
        align="left", baseline="middle", dx=5, color="white", size=10
    ).encode(text="team")

    scatter_plot = (
        alt.layer(scatter_plot, text)
        .configure_view(stroke="transparent")
        .configure_axis(domainWidth=0.8, grid=False)
    )

    st.altair_chart(scatter_plot)

    pca_components = pd.DataFrame(
        pca.components_.T, index=stat_data.columns, columns=["PC1", "PC2"]
    )
    pca_components["feature"] = pca_components.index

    cols = st.columns(2)
    with cols[0]:
        st.subheader("PC1")
        feature_cont_bar_plot = (
            alt.Chart(pca_components).mark_bar().encode(x="feature", y="PC1")
        ).properties(width=500)
        st.altair_chart(feature_cont_bar_plot)

    with cols[1]:
        st.subheader("PC2")
        feature_cont_bar_plot = (
            alt.Chart(pca_components).mark_bar().encode(x="feature", y="PC2")
        ).properties(width=500)
        st.altair_chart(feature_cont_bar_plot)

    st.write(
        "Fonte dati: [understat](https://understat.com/)",
    )


if __name__ == "__main__":
    main()
