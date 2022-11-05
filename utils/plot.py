import altair as alt
import pandas as pd


def barplot_if(data, y: str):
    bar_chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(y=alt.Y(y + ":O", sort="-x"), x=alt.X("i_f:Q", axis=None))
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


def grouped_barplot(data: pd.DataFrame, x: str, y: str, color: str, row: str):
    bar_plot = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            y=alt.Y(y, title=None),
            x=alt.X(x, title=None, axis=None),
            color=alt.Color(color, legend=None),
        )
    )

    text = bar_plot.mark_text(
        align="left",
        baseline="middle",
        dx=3,
        # color="white",  # fontStyle="bold", fontSize=20
    ).encode(text=alt.Text(x, format=",.2f"))

    bar_plot = (
        (alt.layer(bar_plot, text))
        .facet(row=alt.Row(row, title=None))
        .configure_view(stroke="transparent")
        .configure_axis(domainWidth=0.8, grid=False)
    )

    return bar_plot
