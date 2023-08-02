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
    voto_min = st.slider(
        "Voto minimo da considerate", min_value=6.0, max_value=7.0, step=0.5, value=6.5
    )
    min_matches = st.slider("Numero minimo di voti", 1, 30, value=20)

    v_data = (
        data[data.Voto >= voto_min][["Nome", "Voto"]]
        .groupby("Nome")
        .count()
        .reset_index()
        .rename(columns={"Voto": "trues"})
        .copy()
    )
    v_data = v_data.merge(
        data[["Nome", "Voto"]].groupby("Nome").count(), on="Nome", how="left"
    )

    v_data = v_data[v_data.Voto >= min_matches].copy()
    col = "Percentuale_voti_utili"
    v_data[col] = (v_data.trues / v_data.Voto).astype(float)
    v_data["text"] = v_data.Percentuale_voti_utili.apply(lambda x: str(round(x, 2)))

    v_data = v_data.iloc[:40].copy()

    cmap1 = LinearSegmentedColormap.from_list(
        "mycmap",
        [
            "#faa001",
            "#0be3b6ff",
        ],
    )
    base = alt.Chart(v_data).mark_bar().encode(y="Nome", x=col, text="text")
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

    cols = st.columns(2)
    player_1 = cols[0].selectbox(label="Giocatore 1", options=v_data.Nome)
    player_2 = cols[1].selectbox(label="Giocatore 2", options=v_data.Nome)

    c_data = v_data[v_data.Nome.isin([player_1, player_2])]

    base_c = alt.Chart(c_data).mark_bar().encode(y="Nome", x=col, text="text")
    chart_c = base_c.mark_bar().properties(width=300) + base_c.mark_text(
        align="left", dx=2, color="white"
    )
    st.altair_chart(chart_c)
    st.markdown("##")

    cols = st.columns([0.8, 0.1])
    cols[1].write(
        "Fonte voti: [fantacalcio.it](https://fantacalcio.it/)",
    )


if __name__ == "__main__":
    main()
