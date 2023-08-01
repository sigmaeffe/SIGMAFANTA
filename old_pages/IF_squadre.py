import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from utils.data import get_teams_if_data
from utils.plot import barplot_if
from utils.const import RC, GRAPHIC_PATH


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
        st.title("INDICE DI FINALIZZAZIONE")

    st.subheader("Quali squadre concretizzano meglio i gol attesi?")

    data = get_teams_if_data()

    bar_plot = barplot_if(data=data, y="team")

    st.altair_chart(bar_plot, use_container_width=True)

    st.header("Com'è calcolato l'indice di finalizzazione?")
    st.write(
        "Semplicemente è il rapporto fra i gol segnati senza rigori (npg) e i gol attesi senza rigori (npxG)."
    )
    st.subheader("Cosa indica?")
    st.write("Ogni quanti npxG una squadra realizza un gol (in media).")

    st.markdown("##")

    st.write(
        "Post di spiegazione: [Instagram](https://www.instagram.com/p/CjA3uLFt85o/?utm_source=ig_web_copy_link)",
        "Articolo: [Blog](http://www.sigmaeffe.it/2022/09/fantacalcio-quali-squadre-di-serie.html)",
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
