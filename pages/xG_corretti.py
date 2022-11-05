import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from utils.const import RC, GRAPHIC_PATH, CALENDAR
from utils.team_idxs import get_teams_indexes
from utils.plot import grouped_barplot
import pandas as pd
import altair as alt


def main():
    plt.rcParams.update(RC)

    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    high_icon = Image.open(GRAPHIC_PATH / "nome_logo_orizzontale.png")
    st.set_page_config(page_icon=icon, page_title="SIGMASUITE", layout="wide")

    cols = st.columns((0.8, 0.2))
    with cols[1]:
        st.image(high_icon, use_column_width=True)
    with cols[0]:
        st.title("npxG corretti")

    cols = st.columns((0.5, 0.5))
    with cols[0]:
        st.write("Prova")
    with cols[1]:
        first_md, last_md = st.slider(
            label="Giornate considerate",
            min_value=1,
            max_value=len(CALENDAR),
            value=(10, 15),
        )

    date_a = CALENDAR[first_md - 1][0]
    date_b = CALENDAR[last_md - 1][1]
    st.write(
        "Considerate le giornate fra la {} (inizio {}) e la {} (fine {})".format(
            first_md, date_a, last_md, date_b
        )
    )

    idxs = get_teams_indexes(date_a=date_a, date_b=date_b)
    real_idxs = idxs[["team", "npxG/90", "npxGA/90"]]
    corrected_idxs = idxs[["team", "npxG_corretti/90", "npxGA_corretti/90"]]
    corrected_idxs.rename(
        columns={"npxG_corretti/90": "npxG/90", "npxGA_corretti/90": "npxGA/90"},
        inplace=True,
    )

    real_idxs["type"] = "reale"
    corrected_idxs["type"] = "corretto"

    data = pd.concat([real_idxs, corrected_idxs], axis=0)

    cols = st.columns((0.5, 0.5))
    with cols[0]:
        st.subheader("npxG corretti / 90")
        bar_plot = grouped_barplot(
            data=data, y="type:N", x="npxG/90:Q", color="type:N", row="team:N"
        )
        st.altair_chart(bar_plot, use_container_width=True)
    with cols[1]:
        st.subheader("npxGA corretti / 90")
        bar_plot = grouped_barplot(
            data=data, y="type:N", x="npxGA/90:Q", color="type:N", row="team:N"
        )

        st.altair_chart(bar_plot, use_container_width=True)

    st.write(
        "Dati: [understat](https://understat.com/)",
    )

    st.markdown("##")

    st.markdown("##")
    bottom_image = Image.open(GRAPHIC_PATH / "nome_logo_slogan_streamlit.png")

    st.markdown("##")
    cols = st.columns((0.2, 0.6, 0.2))
    cols[1].image(bottom_image)


if __name__ == "__main__":
    main()
