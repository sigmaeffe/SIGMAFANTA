import pandas as pd
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap
import altair as alt


def main():
    data = pd.read_csv("./data/voti_22_23.csv", index_col=0)
    data = data[data.Ruolo == "P"]

    st.header("Esplora i migliori portieri da MOD della Serie A 2022-2023")

    exclude_rp = st.checkbox("Escludi giornate con rigori parati", value=True)

    if exclude_rp:
        data = data[data.Rp == 0]

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

    v_data.sort_values(by=col, ascending=False, inplace=True)

    cmap1 = LinearSegmentedColormap.from_list(
        "mycmap",
        [
            "#faa001",
            "#0be3b6ff",
        ],
    )
    chart = alt.Chart(v_data).mark_bar().encode(x="Nome", y=col)

    st.altair_chart(chart)

    st.subheader("Media Voto portieri")

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

    st.write(
        "Fonte voti: [fantacalcio.it](https://fantacalcio.it/)",
    )


if __name__ == "__main__":
    main()
