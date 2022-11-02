import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from utils.const import RC, GRAPHIC_PATH
from bs4 import BeautifulSoup
import json
import requests
import pandas as pd

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
    "Milan",
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

url_base = "https://understat.com/team/"


def get_json(script):
    s_string = script.string

    ind_start = s_string.index("('") + 2
    ind_end = s_string.index("')")

    j_data = s_string[ind_start:ind_end]
    j_data = j_data.encode("utf-8").decode("unicode_escape")
    js_data = json.loads(j_data)

    return js_data


def display_team_data(team: str) -> None:
    url = url_base + team + "/2022"

    page_tree = requests.get(url)
    page_soup = BeautifulSoup(page_tree.content, "lxml")
    scripts = page_soup.find_all("script")

    team_stats_json = get_json(scripts[2])

    team_stats = parse_team_stats(team_stats_json)

    players_stats_json = get_json(scripts[3])
    player_stats = pd.json_normalize(players_stats_json)
    player_stats = player_stats[player_stats.team_title == team]

    all_columns = ['player_name', 'games', 'time', 'goals', 'xG', 'assists', 'xA', 'shots', 'key_passes', 'yellow_cards', 'red_cards', 'npg', 'npxG', 'xGChain', 'xGBuildup']
    int_columns = ['games', 'time', 'goals', 'assists', 'shots', 'key_passes', 'yellow_cards', 'red_cards', 'npg']
    float_columns = ['xG', 'xA', 'npxG', 'xGChain', 'xGBuildup']

    player_stats = player_stats[all_columns]

    for column in int_columns:
        player_stats[column] = player_stats[column].astype('int')

    for column in float_columns:
        player_stats[column] = player_stats[column].astype('float')

    st.dataframe(team_stats)
    player_stats = player_stats.round(2)
    st.dataframe(player_stats)


def parse_team_stats(js_data) -> pd.DataFrame:
    columns = ['situation', 'shots', 'goals', 'xG', 'shots against', 'goals against', 'xGA']
    df_data = []
    for situation, data in js_data['situation'].items():
        situation_data = list(data.values())
        situation_data = [situation] + situation_data[:-1] + list(situation_data[-1].values())
        df_data.append(situation_data)

    df = pd.DataFrame(df_data, columns=columns)

    return df


def main():
    plt.rcParams.update(RC)

    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    high_icon = Image.open(GRAPHIC_PATH / "nome_logo_orizzontale.png")
    st.set_page_config(page_icon=icon, page_title="SIGMASUITE", layout="wide")

    # st.markdown(page_bg, unsafe_allow_html=True)

    cols = st.columns((0.8, 0.2))
    with cols[1]:
        st.image(high_icon, use_column_width=True)
    with cols[0]:
        st.title("Analizzatore squadre")

    cols = st.columns(2)
    with cols[0]:
        team_choice_1 = st.selectbox("Squadra:", TEAMS, key='tc1')
        display_team_data(team=team_choice_1)
    with cols[1]:
        team_choice_2 = st.selectbox("Squadra:", TEAMS, key='tc2')
        display_team_data(team=team_choice_2)


if __name__ == "__main__":
    main()
