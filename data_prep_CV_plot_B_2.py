from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).parent  
DATA_PATH = BASE_DIR / "Part_B"
SAVE_PATH = BASE_DIR / "Report" / "Graphs_2"

SAVE_PATH.mkdir(parents=True, exist_ok=True)

files = {
    "Cs2SO4": "caesium_sulphate_3.xlsx",
    "Li2SO4": "lithium_sulphate_3.xlsx",
    "K2SO4": "potassium_sulphate_3.xlsx",
    "Na2SO4": "sodium_sulphate_3.xlsx"
}

df_dict = {
    key: pd.read_excel(DATA_PATH / filename, engine="openpyxl")
    for key, filename in files.items()
}

df_list = list(df_dict.values())
alpha_values = [0.3, 0.3, 1, 0.3]
color_values = ["blue", "green", "black", "red"]

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "stix"

fig, ax = plt.subplots()

for i, df in enumerate(df_list):
    ax.plot(df.iloc[1:, 0], df.iloc[1:, 1], alpha=alpha_values[i], color=color_values[i])

ax.set_xlabel("Potential/V vs. Ag/AgCl", fontsize=14)
ax.set_ylabel("Current/μA", fontsize=14)

ax.spines["bottom"].set_position(("data", 0))
ax.spines["bottom"].set_color("black")
ax.spines["bottom"].set_linewidth(0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
ax.xaxis.set_label_coords(0.5, -0.05)

ax.legend(
    [
        r"Cs$_2$SO$_4$",
        r"Li$_2$SO$_4$$\cdot$H$_2$O",
        r"K$_2$SO$_4$",
        r"Na$_2$SO$_4$$\cdot10$H$_2$O",
    ],
    fontsize=11,
    loc="upper left",
)

ax.tick_params(axis="both", which="major", labelsize=12)

plt.savefig(SAVE_PATH / "CVs_part_B.png", dpi=300, transparent=True)
plt.close()