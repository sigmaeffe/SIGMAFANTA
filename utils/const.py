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
