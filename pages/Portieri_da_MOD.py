import pandas as pd
import streamlit as st


def main():
    data = pd.read_csv("./data/voti_22_23.csv", index_col=0)
    data = data[data.Ruolo == "P"]

    st.header("Esplora i migliori portieri da MOD della Serie A 2022-2023")

    exclude_rp = st.checkbox("Escludi giornate con rigori parati", value=True)

    if exclude_rp:
        data = data[data.Rp == 0]

    st.subheader("Media Voto portieri")

    min_matches = st.slider("Numero minimo di voti", 1, 30, value=10)

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

    st.dataframe(mv_df)

    st.write(
        "Fonte voti: [fantacalcio.it](https://fantacalcio.it/)",
    )


if __name__ == "__main__":
    main()
