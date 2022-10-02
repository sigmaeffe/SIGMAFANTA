from pathlib import Path

# import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
from utils import get_players_data, get_teams_data

BACKGROUND_COLOR = "#230094"
SECONDARY_COLOR = "#0CFACA"
PRIMARY_COLOR = "#faa001"

GRAPHIC_PATH = Path("C:\\Users\\feder\\SigmaEffe\\Brand_graphic")
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


def main():
    plt.rcParams.update(rc)

    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    high_icon = Image.open(GRAPHIC_PATH / "nome_logo_orizzontale.png")
    st.set_page_config(
        page_icon=icon, page_title="Indice di finalizzazione", layout="wide"
    )

    st.header("Quali squadre concretizzano meglio i gol attesi?")
    cols = st.columns((0.8, 0.2))
    with cols[0]:
        st.title("INDICE DI FINALIZZAZIONE (i_f)")
    with cols[1]:
        st.image(high_icon)

    p_data = get_players_data()
    pen_data = p_data[p_data.goals != p_data.npg]
    pen_data = pen_data[["goals", "npg", "team"]]
    pen_data["penalty_goals"] = pen_data.goals.astype("int") - pen_data.npg.astype(
        "int"
    )
    pen_data = pen_data.groupby(by=["team"])[["penalty_goals"]].sum()

    data = get_teams_data()
    data = data[["team_goals_scored", "team_npxG"]]
    data["team"] = data.index
    data = data.merge(
        right=pen_data, left_on="title", right_on="team", how="left"
    ).fillna(0)
    data["npg"] = data.team_goals_scored - data.penalty_goals
    data["i_f"] = data.npg / data.team_npxG
    data = data.sort_values(by=["i_f"], ascending=False)

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 4))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    sns.barplot(data=data, y="team", x="i_f", orient="h", ax=ax, color="#11ad8e")
    ax.set_xticks([], [])
    ax.set(xlabel="", ylabel="")
    ax.bar_label(
        ax.containers[-1],
        fmt="%.2f",
        label_type="center",
        color="#ffffff",
    )
    for label in ax.yaxis.get_ticklabels():
        label.set_color("#0cfaca")

    st.pyplot(fig, dpi=600)
    # plot = px.bar(data_frame=data, x="i_f", y="team", orientation="h")
    # st.plotly_chart(plot)

    st.header("Com'è calcolato l'indice di finalizzazione?")
    equation = Image.open(
        GRAPHIC_PATH / "..\\Streamlit\\Indice_di_finalizzazione\\formula.png"
    )

    st.columns((0.4, 0.1, 0.4))[1].image(equation, use_column_width=True)
    st.write("npG: gol segnati senza rigori, npxG: gol attesi senza rigori.")
    st.write("##")
    st.write("Qui trovi la spiegazione dell'indice:")
    st.write(
        "Post: [Instagram](https://www.instagram.com/p/CjA3uLFt85o/?utm_source=ig_web_copy_link) Articolo: [Blog](http://www.sigmaeffe.it/2022/09/fantacalcio-quali-squadre-di-serie.html)"
    )

    # st.markdown("##")
    # st.markdown("##")
    # data.index = data.team
    # data = data[["npg", "team_npxG", "i_f"]]
    # data.rename(columns={"team_npxG": "npxG"}, inplace=True)
    # data.npg = data.npg.astype("int")
    # st.header("Tutti i dati")
    # st.dataframe(
    #     data=data.style.format(precision=3).apply(
    #         lambda x: [
    #             "background-color: " + PRIMARY_COLOR if x.name == "i_f" else ""
    #             for _ in data.index
    #         ],
    #         axis=0,
    #     )
    # )

    st.markdown("##")
    st.markdown("##")
    st.header("Fonte dati")
    st.write("Understat: [understat.com](https://understat.com/)")

    st.markdown("##")
    st.markdown("##")

    st.header(
        "Creato da [SIGMAEFFE](http://www.sigmaeffe.it): Fantacalcio e Statistica"
    )
    st.header("Seguimi e sostienimi")
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
