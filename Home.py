from pathlib import Path

import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
from utils.data import get_players_data, get_teams_data

BACKGROUND_COLOR = "#230094"
SECONDARY_COLOR = "#0CFACA"
PRIMARY_COLOR = "#faa001"

GRAPHIC_PATH = Path("./graphics")
rc = {
    "axes.facecolor": BACKGROUND_COLOR,
    "axes.edgecolor": BACKGROUND_COLOR,
    "axes.labelcolor": "white",
    "figure.facecolor": BACKGROUND_COLOR,
    "patch.edgecolor": BACKGROUND_COLOR,
    "text.color": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    #    "grid.color": None,
    "font.size": 8,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
}

page_bg = f"""
<style>
.stApp{{
background: rgb(2,0,36);
background: linear-gradient(165deg, rgba(2,0,36,1) 0%, rgba(35,0,148,1) 54%, rgba(12,250,202,1) 100%);
background-attachment: fixed;
backgroun-size: cover
}}
</style>
"""


def main():
    plt.rcParams.update(rc)

    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    high_icon = Image.open(GRAPHIC_PATH / "nome_logo_orizzontale.png")
    st.set_page_config(page_icon=icon, page_title="SIGMASUITE", layout="wide")

    st.markdown(page_bg, unsafe_allow_html=True)

    st.image(high_icon, use_column_width=True)

    st.markdown("##")
    bottom_image = Image.open(GRAPHIC_PATH / "nome_logo_slogan_streamlit.png")

    st.markdown("##")
    cols = st.columns((0.2, 0.6, 0.2))
    cols[1].image(bottom_image)

    st.markdown("##")
    st.markdown("##")
    cols = st.columns((0.3, 0.05, 0.1, 0.05, 0.3))
    cols[1].markdown(
        '<a href="https://www.instagram.com/sigmaeffe"><img alt="Instagram" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width=40>',
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        '<a href="https://www.youtube.com/channel/UCbprtthY7EepkzreoddOTng"><img alt="YouTube" src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg" width=150>',
        unsafe_allow_html=True,
    )
    cols[3].markdown(
        '<a href="https://it.tipeee.com/sigmaeffe"><img alt="Tipeee" src="https://cdn.cdnlogo.com/logos/t/21/tipeee.svg" width=100>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
