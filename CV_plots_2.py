import matplotlib.pyplot as plt
import os
import pandas as pd
from data_prep_2 import df_dict_A1, df_dict_A2

# Constants
SAVE_PATH = "/Users/jamiepersonal/Documents/Electrochemistry/Report/Graphs_2"
LABEL_LIST_A1 = ["Ferrocenemethanol", "Ferrocyanide", "Iron (II)"]
LABEL_LIST_A2 = ["Ferrocene (DCM)", "Ferrocene (DMSO)", "Ferrocene (MeCN)", "FCA with Ferrocene", "FCA (MeCN)"]

# Matplotlib settings
plt.rcParams["font.family"] = "Times New Roman"  # Use Times New Roman font
plt.rcParams["mathtext.fontset"] = "stix"       # Use Stix font for math symbols

def plot_data(data, xlabel, ylabel, key, save_path):
    """
    Create and save a plot for the given data.
    
    Args:
        data (pd.DataFrame): Data to plot (expects two columns for x and y).
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        key (str): Key used for naming the saved file.
        save_path (str): Directory where the plot will be saved.
    """
    try:
        fig, ax = plt.subplots()

        # Plotting the data
        ax.plot(data.iloc[1:, 0], data.iloc[1:, 1])
        ax.set_xlabel(xlabel, fontsize=14)
        ax.set_ylabel(ylabel, fontsize=14)

        # Adding the x-axis at y=0
        ax.spines["bottom"].set_position(("data", 0))
        ax.spines["bottom"].set_color("black")
        ax.spines["bottom"].set_linewidth(0.5)

        # Hide the top and right spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Adding dashed line at y=0
        ax.axhline(0, color="black", linewidth=0.5, linestyle="--")

        # Ensure the x-label is at the bottom of the plot
        ax.xaxis.set_label_coords(0.5, -0.05)

        # Adjust tick parameters
        ax.tick_params(axis="both", which="major", labelsize=12)

        # Save the figure
        os.makedirs(save_path, exist_ok=True)  # Ensure save path exists
        file_path = os.path.join(save_path, f"{key}.png")
        plt.savefig(file_path, dpi=300, transparent=True)
        plt.close()

        print(f"Plot saved: {file_path}")
    except Exception as e:
        print(f"Error plotting or saving for {key}: {e}")

for key, value in df_dict_A1.items():
    plot_data(
        data=value,
        xlabel="Potential/V vs. Ag/AgCl",
        ylabel="Current/μA",
        key=key,
        save_path=SAVE_PATH
    )

for key, value in df_dict_A2.items():
    plot_data(
        data=value,
        xlabel="Potential/V vs. Ag",
        ylabel="Current/μA",
        key=key,
        save_path=SAVE_PATH
    )