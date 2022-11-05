""" Utils for teams performance idxs computation. """

import pandas as pd

from utils.data import URL, get_matches_data


def compute_i0(row, data, team_feat, opponent_feat):
    opponents_data = data[data.team.isin(row.opponents)]
    opponent_average_feat = (
        opponents_data[opponent_feat].values / opponents_data.matches.values
    )
    denominator = opponent_average_feat.sum() / row.matches

    return (row[team_feat] / row.matches) / denominator


def compute_aoi(row, data, feat):
    return data[data.team.isin(row.opponents)][feat].mean()


def compute_0_step(data):
    data["IAk"] = data.apply(
        lambda x: compute_i0(x, data, team_feat="npxG", opponent_feat="npxGA"), axis=1
    )
    data["IDk"] = data.apply(
        lambda x: compute_i0(x, data, team_feat="npxGA", opponent_feat="npxG"), axis=1
    )
    data["Average_Opponent_IA"] = data.apply(
        lambda x: compute_aoi(x, data, feat="IAk"), axis=1
    )
    data["Average_Opponent_ID"] = data.apply(
        lambda x: compute_aoi(x, data, feat="IDk"), axis=1
    )

    return data


def compute_iak(row, data):
    opponents_data = data[data.team.isin(row.opponents)]
    opponents_average_npxGA = (
        opponents_data["npxGA"].values / opponents_data.matches.values
    )
    denominator = (
        opponents_average_npxGA / opponents_data["Average_Opponent_IA"].values
    ).sum()

    return row["npxG"] / denominator


def compute_idk(row, data):
    opponents_data = data[data.team.isin(row.opponents)]
    opponents_average_npxG = (
        opponents_data["npxG"].values / opponents_data.matches.values
    )
    denominator = (
        opponents_average_npxG / opponents_data["Average_Opponent_ID"].values
    ).sum()

    return row["npxGA"] / denominator


def compute_kth_step(data):
    data["Average_Opponent_IA"] = data.apply(
        lambda x: compute_aoi(x, data, feat="IAk"), axis=1
    )
    data["Average_Opponent_ID"] = data.apply(
        lambda x: compute_aoi(x, data, feat="IDk"), axis=1
    )
    data["IAk"] = data.apply(lambda x: compute_iak(x, data), axis=1)
    data["IDk"] = data.apply(lambda x: compute_idk(x, data), axis=1)

    return data


def compute_ia_id(in_data, n_steps):
    data = in_data.copy()
    data["npxG/90"] = data.npxG.values / data.matches.values
    data["npxGA/90"] = data.npxGA.values / data.matches.values
    data = compute_0_step(data)
    for i in range(n_steps):
        data = compute_kth_step(data)

    return data


def get_teams_indexes(date_a: str, date_b: str, url: str = URL) -> pd.DataFrame:
    matches_data = get_matches_data(url=url)
    matches_data["date"] = matches_data.date.apply(lambda x: x.split(" ")[0])
    matches_data = matches_data[
        matches_data.date.between(date_a, date_b, inclusive="both")
    ].reset_index(drop=True)

    teams_data = matches_data.groupby(by=["title"]).sum()
    teams_data["matches"] = teams_data.wins + teams_data.draws + teams_data.loses
    teams_data["team"] = teams_data.index

    matches_data["opponent"] = matches_data.apply(
        lambda x: get_opponent(x, matches_data), axis=1
    )
    teams_data["opponents"] = teams_data.team.apply(
        lambda x: matches_data[matches_data.title == x].opponent.values
    )

    dtsc_data = teams_data[["team", "npxG", "npxGA", "opponents", "matches"]]

    dtsc_data = compute_ia_id(in_data=dtsc_data, n_steps=10)

    dtsc_data = dtsc_data.rename(
        columns={"IAk": "npxG_corretti/90", "IDk": "npxGA_corretti/90"}
    )

    dtsc_data["team"] = dtsc_data.index
    return dtsc_data[
        ["team", "npxG/90", "npxG_corretti/90", "npxGA/90", "npxGA_corretti/90"]
    ]


def get_opponent(row, matches):
    date_matches = matches[(matches.date == row.date) & (matches.title != row.title)]
    date_matches = date_matches[date_matches.npxGA == row.npxG]
    # print(date_matches)
    if date_matches.shape[0] == 1:
        return date_matches.title.values[0]

    assert False
