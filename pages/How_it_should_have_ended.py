import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import base64


def get_nr_goals_simulation(team_xg, n_simulations):
    random_values = np.random.random_sample((len(team_xg), n_simulations))
    random_values = random_values <= team_xg[:, np.newaxis]
    return random_values.sum(axis=0)


def seaborn_plot(df: pd.DataFrame, match_id, transparent: bool):
    g = sns.JointGrid(
        data=df,
        y=match_id.split("-")[0],
        x=match_id.split("-")[1],
        marginal_ticks=False,
        height=10,
        ratio=4,
        palette="coolwarm",
    )

    # # Add the joint and marginal histogram plots
    g.plot_joint(
        sns.histplot,
        discrete=(True, True),
        cbar=True,
        stat="percent",
        palette=[
            "#faa001",
            "#230094",
        ],
        cbar_kws={"shrink": 0.8, "format": "%d%%"},
    )
    g.plot_marginals(
        sns.histplot,
        stat="count",
        palette=[
            "#faa001",
            "#230094",
        ],
    )

    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
    # get the current positions of the joint ax and the ax for the marginal x
    pos_joint_ax = g.ax_joint.get_position()
    pos_marg_x_ax = g.ax_marg_x.get_position()
    # reposition the joint ax so it has the same width as the marginal x ax
    g.ax_joint.set_position(
        [pos_joint_ax.x0, pos_joint_ax.y0, pos_marg_x_ax.width, pos_joint_ax.height]
    )
    # reposition the colorbar using new x positions and y positions of the joint ax
    g.fig.axes[-1].set_position([0.83, pos_joint_ax.y0, 0.07, pos_joint_ax.height])

    plt.savefig(
        f"{match_id}.png", dpi=500, transparent=transparent, bbox_inches="tight"
    )


def generate_simulation_results(url, n_simulations, transparent):
    shoots = pd.read_html(url, header=1)[-3]
    shoots = shoots[~shoots.Giocatore.isna()]

    teams = shoots.Squadra.unique()

    team_a_shoots_xg = shoots[shoots.Squadra == teams[0]].xG.to_numpy()
    team_b_shoots_xg = shoots[shoots.Squadra == teams[1]].xG.to_numpy()

    sim_team_a = get_nr_goals_simulation(team_a_shoots_xg, n_simulations=n_simulations)
    sim_team_b = get_nr_goals_simulation(team_b_shoots_xg, n_simulations=n_simulations)

    df = pd.DataFrame({teams[0]: sim_team_a, teams[1]: sim_team_b})

    match_id = url.split("/")[-1]
    y = match_id.split("-")[0]
    x = match_id.split("-")[1]

    df["Result"] = df.apply(lambda row: f"{row[y]}-{row[x]}", axis=1)

    df = df[df[teams[0]] <= 5]
    df = df[df[teams[1]] <= 5]

    seaborn_plot(df=df, match_id=match_id, transparent=transparent)

    fig = px.density_heatmap(
        df,
        y=y,
        x=x,
        marginal_x="histogram",
        marginal_y="histogram",
        histnorm="percent",
        color_continuous_scale=[
            "#faa001",
            "#230094",
        ],  # Use the same color for start and end
    )

    st.plotly_chart(fig)

    results_counts = df.Result.value_counts()
    results_percentage = results_counts / df.shape[0]
    results_percentage.rename("Result %", inplace=True)
    results_percentage.sort_values(ascending=False, inplace=True)
    results_percentage = results_percentage.apply(lambda x: round(x * 100, 2))

    return results_percentage, match_id


def main():
    st.title("Match Simulation App")

    url = st.text_input("Enter the URL:")
    n_simulations = st.number_input(
        "Number of Simulations:", min_value=1, value=1000000
    )
    transparent = st.checkbox("Transparent Plot", value=True)

    if st.button("Run Simulation"):
        with st.spinner("Running Simulation..."):
            df, match_id = generate_simulation_results(url, n_simulations, transparent)

        st.success(f"Simulation completed for match ID: {match_id}")

        st.subheader("Simulation Results:")
        st.dataframe(df)

        st.subheader("Download Files:")
        st.markdown(
            get_table_download_link(df.to_csv(), file_name="results_perc.csv"),
            unsafe_allow_html=True,
        )
        st.markdown(
            get_image_download_link(file_name=f"{match_id}.png"), unsafe_allow_html=True
        )


def get_table_download_link(csv_data, file_name="downloaded_file.csv"):
    """Generates a link allowing the data in a given Pandas dataframe to be downloaded."""
    b64 = base64.b64encode(csv_data.encode()).decode()  # Encode CSV data as base64
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Download {file_name}</a>'
    return href


def get_image_download_link(file_name="downloaded_image.png"):
    """Generates a link allowing the image file to be downloaded."""
    with open(file_name, "rb") as f:
        image_data = f.read()
    b64_image = base64.b64encode(image_data).decode()
    href = f'<a href="data:image/png;base64,{b64_image}" download="{file_name}">Download {file_name}</a>'
    return href


if __name__ == "__main__":
    main()
