import altair as alt


def barplot_if(data, y: str):
    bar_chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            y=alt.Y(y + ":O", sort="-x"),
            x=alt.X("i_f:Q", axis=None)
            # color="EnergyType:N"
        )
    )

    text = bar_chart.mark_text(
        align="left",
        baseline="middle",
        dx=3,
        color="white",  # fontStyle="bold", fontSize=20
    ).encode(text=alt.Text("i_f:Q", format=",.2f"))

    bar_plot = (
        alt.layer(bar_chart, text)
        .configure_view(stroke="transparent")
        .configure_axis(domainWidth=0.8, grid=False)
    )

    return bar_plot
