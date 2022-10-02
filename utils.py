from bs4 import BeautifulSoup
import json
import requests
import pandas as pd

UNDERSTAT_MATCHES_FEATURES_DICT = {
    "deep": "deep_completions",
    "deep_allowed": "deep_completions_allowed",
    "scored": "goals_scored",
    "missed": "goals_conceded",
    "title": "team",
}


URL = "https://understat.com/league/Serie_A"


def get_players_data(url: str = URL) -> pd.DataFrame:
    page_tree = requests.get(url)
    page_soup = BeautifulSoup(page_tree.content, "lxml")
    scripts = page_soup.find_all("script")

    return _get_players_data(scripts=scripts)


def get_json_data(script) -> pd.DataFrame:
    s_string = script.string

    ind_start = s_string.index("('") + 2
    ind_end = s_string.index("')")

    j_data = s_string[ind_start:ind_end]
    j_data = j_data.encode("utf-8").decode("unicode_escape")
    js_data = json.loads(j_data)
    if type(js_data) == list:
        data = pd.json_normalize(js_data)
    elif type(js_data) == dict:
        data = pd.json_normalize(js_data.values())

    return data


def _get_players_data(scripts) -> pd.DataFrame:
    players_data = get_json_data(scripts[3])
    players_data.drop(columns=["id"], inplace=True)
    players_data.rename(columns={"team_title": "team"}, inplace=True)

    int_c = [
        "games",
        "time",
        "goals",
        "assists",
        "shots",
        "key_passes",
        "yellow_cards",
        "red_cards",
        "npg",
    ]
    float_c = ["xG", "xA", "npxG", "xGChain", "xGBuildup"]

    for c in int_c:
        players_data[c] = players_data[c].astype("int")

    for c in float_c:
        players_data[c] = players_data[c].astype("float")

    return players_data


def _get_matches_data(scripts) -> pd.DataFrame:
    matches_data = get_json_data(scripts[2])
    matches_data = matches_data.explode("history")
    h = matches_data.pop("history")
    matches_data = pd.concat(
        [matches_data.reset_index(drop=True), pd.DataFrame(h.tolist())], axis=1
    )

    return matches_data


def get_teams_data(url: str = URL) -> pd.DataFrame:
    page_tree = requests.get(url)
    page_soup = BeautifulSoup(page_tree.content, "lxml")
    scripts = page_soup.find_all("script")

    matches_data = _get_matches_data(scripts=scripts)

    teams_data = matches_data.groupby("title").sum()
    teams_data.rename(columns=UNDERSTAT_MATCHES_FEATURES_DICT, inplace=True)
    teams_data.rename(
        columns={column: "team_" + column for column in teams_data.columns},
        inplace=True,
    )

    return teams_data
