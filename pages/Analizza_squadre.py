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

    teams_data = get_teams_data()
    players_data = get_players_data(separate_multi_team_players=True)
    full_teams_data = (
        players_data.groupby("team")
        .sum()[
            [
                "shots",
                "npg",
                "assists",
                "xA",
                "xGChain",
                "xGBuildup",
                "red_cards",
                "yellow_cards",
                "key_passes",
            ]
        ]
        .join(teams_data)
    )

    full_teams_data.rename(
        columns={c: c[5:] if "team" in c else c for c in full_teams_data.columns},
        inplace=True,
    )

    st.dataframe(full_teams_data.style.format(precision=2))

    full_teams_data["npg/npxG"] = full_teams_data.npg / full_teams_data.npxG

    full_teams_data["Rigori concessi"] = (
        (full_teams_data.xG - (full_teams_data.npxG)) / 0.76
    ).astype("int")
    full_teams_data["npShots"] = (
        full_teams_data.shots - full_teams_data["Rigori concessi"]
    )

    full_teams_data["npxG/npShots"] = full_teams_data.npxG / full_teams_data.npShots

    full_teams_data["n_matches"] = (
        full_teams_data.wins + full_teams_data.draws + full_teams_data.loses
    )
    full_teams_data["npShots/90"] = full_teams_data.npShots / full_teams_data.n_matches

    full_teams_data["npxG/90"] = full_teams_data.npxG / full_teams_data.n_matches
    full_teams_data["npg/90"] = full_teams_data.npg / full_teams_data.n_matches

    full_teams_data["KP/90"] = full_teams_data.key_passes / full_teams_data.n_matches
    full_teams_data["xA/90"] = full_teams_data.xA / full_teams_data.n_matches
    full_teams_data["assists/90"] = full_teams_data.assists / full_teams_data.n_matches
    full_teams_data["xA/KP"] = full_teams_data.xA / full_teams_data.key_passes
    full_teams_data["assists/KP"] = full_teams_data.assists / full_teams_data.key_passes

    full_teams_data["xGA/90"] = full_teams_data.xGA / full_teams_data.n_matches
    full_teams_data["GA/xGA"] = full_teams_data.goals_conceded / full_teams_data.xGA
    full_teams_data["GA/90"] = (
        full_teams_data.goals_conceded / full_teams_data.n_matches
    )
    full_teams_data["yellow_cards/90"] = (
        full_teams_data.yellow_cards / full_teams_data.n_matches
    )
    full_teams_data["red_cards/90"] = (
        full_teams_data.red_cards / full_teams_data.n_matches
    )

    st.header("Goal")

    fin_data = full_teams_data[
        [
            "npShots/90",
            "npxG/npShots",
            "npxG/90",
            "npg/90",
            "npg/npxG",
            "Rigori concessi",
        ]
    ]

    st.dataframe(fin_data.style.format(precision=2))

    st.header("Assist")

    as_data = full_teams_data[["KP/90", "xA/90", "assists/90", "xA/KP", "assists/KP"]]

    st.dataframe(as_data.style.format(precision=2))

    st.header("Difesa")

    def_data = full_teams_data[["xGA/90", "GA/90", "GA/xGA"]]

    st.dataframe(def_data.style.format(precision=2))

    st.header("Cartellini")

    card_data = full_teams_data[
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
        "deep_completions",
        "xGChain",
        "xGBuildup",
    ]
    stat_def_columns = ["xGA", "deep_completions_allowed"]

    stat_data = full_teams_data[stat_def_columns + stat_at_columns]

    pca = PCA(n_components=2)
    scaler = StandardScaler()
    scaled_data = pd.DataFrame(
        scaler.fit_transform(stat_data), columns=stat_data.columns
    )
    pca_data = pd.DataFrame(pca.fit_transform(scaled_data), columns=["PC1", "PC2"])

    print(type(pca_data))
    pca_data["team"] = full_teams_data.index

    st.write(
        "PCA explained variance: "
        + str(round(sum(pca.explained_variance_ratio_) * 100, 2))
        + "%"
    )

    scatter_plot = (
        alt.Chart(pca_data).mark_point(size=100).encode(x="PC1:Q", y="PC2:Q")
    ).properties(width=700, height=700)

    text = scatter_plot.mark_text(
        align="left", baseline="middle", dx=7, color="white"
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

    st.subheader("PC1")
    feature_cont_bar_plot = (
        alt.Chart(pca_components).mark_bar().encode(x="feature", y="PC1")
    ).properties(width=500)
    st.altair_chart(feature_cont_bar_plot)

    st.subheader("PC2")
    feature_cont_bar_plot = (
        alt.Chart(pca_components).mark_bar().encode(x="feature", y="PC2")
    ).properties(width=500)
    st.altair_chart(feature_cont_bar_plot)

    st.header("Trend analysis")
    matches_data = get_matches_data()

    cols = st.columns(2)
    with cols[0]:
        team_choice = st.selectbox("Squadra:", TEAMS, key="tc")
    with cols[1]:
        feature_choice = st.selectbox("Feature:", matches_data.columns, key="fc")

    team_data = (
        matches_data[matches_data.title == team_choice]
        .sort_values(by="date", ascending=False)
        .copy()
    )
    team_data["matchday"] = range(1, team_data.shape[0] + 1)

    line_chart = (
        alt.Chart(team_data)
        .mark_line(color="#ffffff")
        .encode(x="matchday", y=feature_choice)
        .properties(width=1000)
    )
    s_team_data = team_data.copy()
    s_team_data[feature_choice] = (
        s_team_data[feature_choice].rolling(5, center=True).mean()
    )
    smoothed_line_chart = (
        alt.Chart(s_team_data)
        .mark_line(color="#faa001")
        .encode(x="matchday", y=feature_choice)
        .properties(width=1000)
    )

    st.altair_chart(line_chart + smoothed_line_chart)

    st.write(
        "Fonte dati: [understat](https://understat.com/)",
    )


if __name__ == "__main__":
    main()
