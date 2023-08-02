import pandas as pd
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap
import altair as alt


def main():
    data = pd.read_csv("./data/voti_22_23.csv", index_col=0)
    data = data[data.Ruolo == "D"]
    print(data)
    exclude_bonus = st.checkbox("Escludi giornate con bonus", value=True)

    if exclude_bonus:
        data = data[(data.Gf == 0) & (data.Ass == 0)]

    st.header("Esplora i migliori difensori da MOD della Serie A 2022-2023")

    st.subheader("Voti utili per il modificatore di difesa")

    voto_mins = [6.0, 6.5, 7.0]
    voto_min = st.slider(
        "Voto minimo da considerate",
        min_value=voto_mins[0],
        max_value=voto_mins[2],
        step=0.5,
        value=voto_mins[1],
    )
    min_matches = st.slider("Numero minimo di voti", 1, 30, value=20)
    col = "Percentuale_voti_utili"

    choosen_min_data = (
        data[data.Voto >= voto_min][["Nome", "Voto"]]
        .groupby("Nome")
        .count()
        .reset_index()
        .rename(columns={"Voto": "trues"})
        .copy()
    )
    choosen_min_data = choosen_min_data.merge(
        data[["Nome", "Voto"]].groupby("Nome").count(), on="Nome", how="left"
    )
    choosen_min_data = choosen_min_data[choosen_min_data.Voto >= min_matches].copy()

    choosen_min_data[col] = (choosen_min_data.trues / choosen_min_data.Voto).astype(
        float
    )
    choosen_min_data["text"] = choosen_min_data[col].apply(lambda x: str(round(x, 2)))

    all_v_data = []
    for v in voto_mins:
        v_data = (
            data[data.Voto >= v][["Nome", "Voto"]]
            .groupby("Nome")
            .count()
            .reset_index()
            .rename(columns={"Voto": "trues"})
            .copy()
        )
        v_data = v_data.merge(
            data[["Nome", "Voto"]].groupby("Nome").count(), on="Nome", how="left"
        )
        v_data["min_voto"] = f">={v}"

        v_data = v_data[v_data.Voto >= min_matches].copy()

        v_data[col] = (v_data.trues / v_data.Voto).astype(float)

        all_v_data.append(v_data)
    all_v_data = pd.concat(all_v_data)

    choosen_min_data.sort_values(by=col, ascending=False, inplace=True)
    choosen_min_data = choosen_min_data.iloc[:40]

    cmap1 = LinearSegmentedColormap.from_list(
        "mycmap",
        [
            "#faa001",
            "#0be3b6ff",
        ],
    )
    base = (
        alt.Chart(choosen_min_data)
        .mark_bar()
        .encode(y=alt.Y("Nome"), x=alt.X(col), text="text")
    )
    chart = base.mark_bar().properties(width=300) + base.mark_text(
        align="left", dx=2, color="white"
    )
    st.altair_chart(chart)

    st.subheader("Media Voto difensori")

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

    st.subheader("Confronta giocatori")

    all_v_data.sort_values(by=col, ascending=False, inplace=True)

    cols = st.columns(2)
    names = all_v_data.Nome
    player_1 = cols[0].selectbox(label="Giocatore 1", options=names, index=0)
    player_2 = cols[1].selectbox(label="Giocatore 2", options=names, index=1)

    c_data = all_v_data[all_v_data.Nome.isin([player_1, player_2])]
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
    chart_c = base_c.mark_bar()  # + base_c.mark_text(align="left", dx=2, color="white")
    st.altair_chart(chart_c)
    st.markdown("##")

    cols = st.columns([0.8, 0.1])
    cols[1].write(
        "Fonte voti: [fantacalcio.it](https://fantacalcio.it/)",
    )


if __name__ == "__main__":
    main()
