from pathlib import Path

BACKGROUND_COLOR = "#230094"
SECONDARY_COLOR = "#0CFACA"
PRIMARY_COLOR = "#faa001"

GRAPHIC_PATH = Path("./graphics")
RC = {
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

CALENDAR = (
    ("2022-08-13", "2022-08-15"),
    ("2022-08-20", "2022-08-22"),
    ("2022-08-26", "2022-08-28"),
    ("2022-08-30", "2022-09-01"),
    ("2022-09-03", "2022-09-05"),
    ("2022-09-10", "2022-09-12"),
    ("2022-09-16", "2022-09-18"),
    ("2022-10-01", "2022-10-03"),
    ("2022-10-08", "2022-10-10"),
    ("2022-10-15", "2022-10-17"),
    ("2022-10-21", "2022-10-24"),
    ("2022-10-29", "2022-10-31"),
    ("2022-11-04", "2022-11-06"),
    ("2022-11-08", "2022-11-10"),
    ("2022-11-11", "2022-11-13"),
)
