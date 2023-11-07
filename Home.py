import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from utils.const import (
    GRAPHIC_PATH,
    RC,
)
from utils.mod import LINK_STYLE

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
    plt.rcParams.update(RC)

    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    high_icon = Image.open(GRAPHIC_PATH / "nome_logo_orizzontale.png")

    st.set_page_config(page_icon=icon, page_title="SIGMASUITE", layout="wide")

    st.markdown(page_bg, unsafe_allow_html=True)

    cols = st.columns((0.1, 0.8, 0.1))
    cols[1].image(high_icon, use_column_width=True)

    bottom_image = Image.open(GRAPHIC_PATH / "nome_logo_slogan_streamlit.png")

    cols = st.columns((0.2, 0.6, 0.2))
    cols[1].image(bottom_image)

    st.markdown("##")
    # st.write("Nel menu a sinistra trovi tutte le SIGMAPP.")
    st.markdown(LINK_STYLE, unsafe_allow_html=True)
    # st.markdown(
    #     '<a href="/Portieri_da_MOD" target="_self" class="custom-link">Portieri da MOD</a>',
    #     unsafe_allow_html=True,
    # )

    # st.markdown(
    #     '<a href="/Difensori_da_MOD" target="_self" class="custom-link">Difensori da MOD</a>',
    #     unsafe_allow_html=True,
    # )

    st.header("Benvenuto/a nella suite di analisi!")

    st.markdown("##")
    st.markdown("##")
    cols = st.columns((0.2, 0.04, 0.04, 0.06, 0.08, 0.2))
    cols[1].markdown(
        '<a href="https://www.instagram.com/sigmaeffe"><img alt="Instagram" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width=40>',
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        '<a href="https://twitter.com/sigmaeffe"><img alt="Twitter" src="https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg" width=40>',
        unsafe_allow_html=True,
    )
    cols[3].markdown(
        '<a href="https://it.tipeee.com/sigmaeffe"><img alt="Tipeee" src="https://cdn.cdnlogo.com/logos/t/21/tipeee.svg" width=100>',
        unsafe_allow_html=True,
    )
    cols[4].markdown(
        '<a href="https://medium.com/@markfootballdata"><img alt="Medium" src="https://upload.wikimedia.org/wikipedia/commons/0/0d/Medium_%28website%29_logo.svg" width=140>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
