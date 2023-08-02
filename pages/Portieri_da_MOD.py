import pandas as pd
import streamlit as st
from utils.mod import (
    create_v_data,
    make_voto_mins_matches_slider,
    VOTO_MINS,
    make_bar_chart_choosen_voto,
    make_df_mv_display,
    make_bottom,
    make_players_compare,
)


def main():
    data = pd.read_csv("./data/voti_22_23.csv", index_col=0)
    data = data[data.Ruolo == "P"]

    st.header("Esplora i migliori portieri da MOD della Serie A 2022-2023")

    exclude_rp = st.checkbox("Escludi giornate con rigori parati", value=True)

    if exclude_rp:
        data = data[data.Rp == 0]

        st.header("Esplora i migliori difensori da MOD della Serie A 2022-2023")

    st.subheader("Voti utili per il modificatore di difesa")

    voto_min, min_matches = make_voto_mins_matches_slider()

    col = "Percentuale_voti_utili"

    choosen_min_data = create_v_data(
        df=data, voto_min=voto_min, col=col, min_matches=min_matches
    )

    choosen_min_data.sort_values(by=col, ascending=False, inplace=True)
    choosen_min_data = choosen_min_data.iloc[:40]

    all_v_data = pd.concat(
        [
            create_v_data(df=data, voto_min=v, col=col, min_matches=min_matches)
            for v in VOTO_MINS
        ]
    )

    make_bar_chart_choosen_voto(data=choosen_min_data, col=col)

    st.subheader("Media Voto difensori")
    make_df_mv_display(data=data, min_matches=min_matches)

    st.subheader("Confronta difensori")

    make_players_compare(data=all_v_data, col=col)

    make_bottom()


if __name__ == "__main__":
    main()
