import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from utils.const import RC, GRAPHIC_PATH
from utils.data import get_players_data

from typing import Dict


def main():
    plt.rcParams.update(RC)

    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    high_icon = Image.open(GRAPHIC_PATH / "nome_logo_orizzontale.png")
    st.set_page_config(page_icon=icon, page_title="SIGMASUITE", layout="wide")

    # st.markdown(page_bg, unsafe_allow_html=True)

    cols = st.columns((0.8, 0.2))
    with cols[1]:
        st.image(high_icon, use_column_width=True)
    with cols[0]:
        st.title("Assist vs KP")

    data = get_players_data()

    st.dataframe(data)


if __name__ == "__main__":
    main()
