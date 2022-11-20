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


def get_players_data(
    url: str = URL, separate_multi_team_players: bool = False
) -> pd.DataFrame:
    page_tree = requests.get(url)
    page_soup = BeautifulSoup(page_tree.content, "lxml")
    scripts = page_soup.find_all("script")

    return _get_players_data(
        scripts=scripts, separate_multi_team_players=separate_multi_team_players
    )


def get_players_if_data(min_goal: int = 0) -> pd.DataFrame:
    data = get_players_data()
    data["i_f"] = data.npg / data.npxG
    data = data.sort_values(by=["i_f"], ascending=False)
    data = data[data.npg >= min_goal]
    return data


def get_teams_if_data() -> pd.DataFrame:
    p_data = get_players_data()
    pen_data = p_data[p_data.goals != p_data.npg]
    pen_data = pen_data[["goals", "npg", "team"]]
    pen_data["penalty_goals"] = pen_data.goals.astype("int") - pen_data.npg.astype(
        "int"
    )
    pen_data = pen_data.groupby(by=["team"])[["penalty_goals"]].sum()

    data = get_teams_data()
    data = data[["team_goals_scored", "team_npxG"]]
    data["team"] = data.index
    data = data.merge(
        right=pen_data, left_on="title", right_on="team", how="left"
    ).fillna(0)
    data["npg"] = data.team_goals_scored - data.penalty_goals
    data["i_f"] = data.npg / data.team_npxG
    data = data.sort_values(by=["i_f"], ascending=False)

    return data


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


def _get_players_data(scripts, separate_multi_team_players: bool) -> pd.DataFrame:
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

    if separate_multi_team_players:
        to_append = []
        for idx in players_data[players_data.team.str.contains(",")].index:
            row = players_data.loc[idx]
            row_teams = row.team.split(",")
            players_data.loc[idx, "team"] = row_teams[0]
            for i in range(1, len(row_teams)):
                r_copy = row.copy()
                r_copy.team = row_teams[i]

                to_append.append(r_copy)
        to_append = pd.concat(to_append, axis=1).T
        players_data = pd.concat([players_data, to_append]).reset_index(drop=True)

    return players_data


def _get_matches_data(scripts) -> pd.DataFrame:
    matches_data = get_json_data(scripts[2])
    matches_data = matches_data.explode("history")
    h = matches_data.pop("history")
    matches_data = pd.concat(
        [matches_data.reset_index(drop=True), pd.DataFrame(h.tolist())], axis=1
    )

    return matches_data


def get_matches_data(url: str = URL) -> pd.DataFrame:
    page_tree = requests.get(url)
    page_soup = BeautifulSoup(page_tree.content, "lxml")
    scripts = page_soup.find_all("script")

    matches_data = _get_matches_data(scripts=scripts)

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
