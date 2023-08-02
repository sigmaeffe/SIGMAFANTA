"""Utils for MOD."""
import pandas as pd
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap
import altair as alt

VOTO_MINS = [6.0, 6.5, 7.0]


def create_v_data(
    df: pd.DataFrame, voto_min: float, col: str, min_matches: int
) -> pd.DataFrame:
    v_data = (
        df[df.Voto >= voto_min][["Nome", "Voto"]]
        .groupby("Nome")
        .count()
        .reset_index()
        .rename(columns={"Voto": "trues"})
        .copy()
    )
    v_data = v_data.merge(
        df[["Nome", "Voto"]].groupby("Nome").count(), on="Nome", how="left"
    )
    v_data = v_data[v_data.Voto >= min_matches].copy()

    v_data[col] = (v_data.trues / v_data.Voto).astype(float)
    v_data["text"] = v_data[col].apply(lambda x: str(round(x, 2)))
    v_data["min_voto"] = f">={voto_min}"
    return v_data


def make_voto_mins_matches_slider(voto_mins=VOTO_MINS):
    voto_min = st.slider(
        "Voto minimo da considerate",
        min_value=voto_mins[0],
        max_value=voto_mins[2],
        step=0.5,
        value=voto_mins[1],
    )
    min_matches = st.slider("Numero minimo di voti", 1, 30, value=20)

    return voto_min, min_matches


def make_bar_chart_choosen_voto(data: pd.DataFrame, col: str):
    base = alt.Chart(data).mark_bar().encode(y=alt.Y("Nome"), x=alt.X(col), text="text")
    chart = base.mark_bar().properties(width=300) + base.mark_text(
        align="left", dx=2, color="white"
    )
    st.altair_chart(chart)


def make_df_mv_display(data: pd.DataFrame, min_matches: int):
    cmap1 = LinearSegmentedColormap.from_list(
        "mycmap",
        [
            "#faa001",
            "#0be3b6ff",
        ],
    )

    mv_df = (
        data[["Nome", "Voto"]]
        .groupby("Nome")
        .mean()
        .reset_index(drop=False)
        .rename(columns={"Voto": "MV"})
    )
    mv_df = mv_df.merge(
        data[["Nome", "Voto"]]
        .groupby("Nome")
        .count()
        .reset_index(drop=False)
        .rename(columns={"Voto": "Numero voti"})
    )
    mv_df = mv_df[mv_df["Numero voti"] >= min_matches]
    mv_df.sort_values("MV", ascending=False, inplace=True)

    formatted_mv__df = mv_df.style.format(precision=2).background_gradient(
        subset=["MV"], cmap=cmap1
    )

    st.dataframe(formatted_mv__df)


def make_bottom():
    st.markdown("##")

    cols = st.columns([0.3, 0.1])
    cols[1].write(
        "Fonte voti: [fantacalcio.it](https://fantacalcio.it/)",
    )


def make_players_compare(data: pd.DataFrame, col: str):
    data.sort_values(by=col, ascending=False, inplace=True)

    cols = st.columns(2)
    names = data.Nome
    player_1 = cols[0].selectbox(label="Giocatore 1", options=names, index=0)
    player_2 = cols[1].selectbox(label="Giocatore 2", options=names, index=1)

    c_data = data[data.Nome.isin([player_1, player_2])]
    print(c_data)

    base_c = (
        alt.Chart(c_data)
        .mark_bar(color="white")
        .encode(
            x=alt.X("Nome", axis=None),
            y=col,
            color="Nome",
            column=alt.Column(
                "min_voto", header=alt.Header(labelColor="white", labelFontSize=15)
            ),
        )
    )
    chart_c = base_c.mark_bar()
    st.altair_chart(chart_c)
