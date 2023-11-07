from itertools import product
from typing import Sequence
import streamlit as st
from utils.data import get_teams_data, get_players_data
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.stats import poisson
import plotly.express as px


def draw_top_k_stat(
    players_data: pd.DataFrame, stat_name: str, right: bool, k: int = 5
):
    st.markdown(f"#### Top {k} giocatori per {stat_name}")
    top_npxg_data = players_data.sort_values(by=stat_name, ascending=False)[:k]
    top_npxg_data.sort_values(by=stat_name, ascending=True, inplace=True)
    topnpxg_fig = go.Figure(
        [
            go.Bar(
                x=top_npxg_data[stat_name].values,
                y=top_npxg_data.player_name.values,
                orientation="h",
                text=top_npxg_data[stat_name].values,
                textfont=dict(color="white"),
            )
        ]
    )
    topnpxg_fig.update_layout(
        width=250,
    )
    if right:
        topnpxg_fig.update_xaxes(autorange="reversed")
        topnpxg_fig.update_yaxes(side="right")
    topnpxg_fig.update_xaxes(showticklabels=False)

    st.plotly_chart(topnpxg_fig)


def team_page(
    column,
    teams: Sequence[str],
    key: str,
    teams_data: pd.DataFrame,
    players_data: pd.DataFrame,
    right: bool = False,
):
    with column:
        team = st.selectbox(label="-", options=teams, key=key)
        team_data = teams_data.loc[team]
        team_players_data = players_data[players_data.team == team].copy()
        team_players_data["xGChain %"] = (
            team_players_data.xGChain / team_data.xG * 100
        ).round(2)

        team_stats_fig = go.Figure(
            [
                go.Bar(
                    x=team_data.values,
                    y=team_data.index,
                    orientation="h",
                )
            ]
        )
        team_stats_fig.update_layout(
            width=350,
        )
        if right:
            team_stats_fig.update_xaxes(autorange="reversed")
            team_stats_fig.update_yaxes(side="right")
            # team_stats_fig.update_yaxes(showticklabels=False)

        st.markdown("#### Statistiche di squadra")
        st.plotly_chart(team_stats_fig)

        draw_top_k_stat(players_data=team_players_data, stat_name="npxG", right=right)
        draw_top_k_stat(players_data=team_players_data, stat_name="xA", right=right)
        draw_top_k_stat(
            players_data=team_players_data, stat_name="xGChain %", right=right
        )

        stat_name_choose = st.selectbox(
            label="stat_name_choose",
            options=team_players_data.columns,
            key=f"{key}_stat",
            index=1,
        )
        draw_top_k_stat(
            players_data=team_players_data, stat_name=stat_name_choose, right=right
        )

        return team, team_data.xG / (team_data.wins + team_data.draws + team_data.loses)


def main():
    players_data = get_players_data().round(2)
    teams_data = get_teams_data()
    teams_data = teams_data.round(2)
    teams_data.columns = [c[5:] for c in teams_data.columns]

    st.header(
        "Benvenuto nel tool per lo studio delle partite, usando i dati di understat.com"
    )
    st.write("Seleziona le due squadre")

    # st.table(players_data)

    # st.table(teams_data)

    teams = teams_data.index.to_numpy()
    columns = st.columns(2)
    team_1, xg1 = team_page(
        column=columns[0],
        teams=teams,
        key=0,
        players_data=players_data,
        teams_data=teams_data,
    )
    team_2, xg2 = team_page(
        column=columns[1],
        teams=teams,
        key=1,
        players_data=players_data,
        teams_data=teams_data,
        right=True,
    )

    st.markdown("## Analisi predittiva")
    st.markdown("### Modello 1: xGM")
    st.write(
        "Questo modello è preso da [qui](https://www.jsr.org/index.php/path/article/view/1116) ed è un semplice modello poissoniano che usa come media gli xGP90 di una squadra"
    )

    MAX_GOLS = 7
    g1 = np.zeros(MAX_GOLS + 1)
    g2 = np.zeros(MAX_GOLS + 1)

    for k in range(MAX_GOLS + 1):
        g1[k] = poisson.pmf(k=k, mu=xg1)
        g2[k] = poisson.pmf(k=k, mu=xg2)

    results_matrix = np.zeros((MAX_GOLS + 1, MAX_GOLS + 1))
    for i, j in product(range(MAX_GOLS + 1), range(MAX_GOLS + 1)):
        results_matrix[i, j] = g1[i] * g2[j]

    results_matrix *= 100
    result_matrix_fig = px.imshow(results_matrix.round(2), text_auto=True)
    result_matrix_fig.update_xaxes(title="Trasferta")
    result_matrix_fig.update_yaxes(title="Casa")
    result_matrix_fig.update_layout(width=1000, height=700)
    st.plotly_chart(result_matrix_fig)

    prob_hwin = np.sum(np.triu(results_matrix.T, k=1))
    prob_awin = np.sum(np.triu(results_matrix, k=1))
    prob_draw = np.sum(np.diag(results_matrix))

    fig_1x2_probs = px.bar(
        x=["vince casa", "pareggio", "vince_trasferta"],
        y=[prob_hwin, prob_draw, prob_awin],
    )
    st.plotly_chart(fig_1x2_probs)

    max_prob_result = np.unravel_index(np.argmax(results_matrix), results_matrix.shape)
    st.write(
        f"Il risultato più probabile per {team_1} vs {team_2} è "
        + f"{max_prob_result[0]}-{max_prob_result[1]}, "
        + f"con probabilità {results_matrix.max().round(2)}%"
    )

    st.write(
        "La maggiore limitazione di questo modello è che non considera la forza difensiva dell'avversario"
    )


if __name__ == "__main__":
    main()
