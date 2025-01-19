from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Dynamically set the folder paths relative to the script's location
BASE_DIR = Path(__file__).parent  # Directory where this script is located
DATA_PATH = BASE_DIR / "Data" / "Part_B"
SAVE_PATH = BASE_DIR / "Report" / "Graphs_2"

# Ensure the save path exists
SAVE_PATH.mkdir(parents=True, exist_ok=True)

# pH values to process
pH_list = [3, 6, 9, 12]

# Collect files for each pH value
files_for_pH = []

for file in DATA_PATH.glob("*.xlsx"):
    for i in pH_list:
        if f"potassium_sulphate_pH_{i}" in file.name:
            files_for_pH.append(file)

# Sort files based on pH values
files_for_pH.sort(key=lambda x: int(x.stem.split("potassium_sulphate_pH_")[1]))

# Create a dictionary to store DataFrames for each pH value
df_dict = {}

for i, file in enumerate(files_for_pH):
    df_dict[pH_list[i]] = pd.read_excel(file, engine="openpyxl")

# Matplotlib settings
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "stix"

# Plotting data
fig, ax = plt.subplots()

alpha_values = [0.8, 0.8, 1, 0.8]
color_values = ['#80CBC4', '#FFDAB9', 'black', '#D8B1D2']

for i, (key, df) in enumerate(df_dict.items()):
    ax.plot(df.iloc[1:, 0], df.iloc[1:, 1], alpha=alpha_values[i], color=color_values[i])

# Configure plot axes and labels
ax.set_xlabel("Potential/V vs. Ag/AgCl", fontsize=14)
ax.set_ylabel("Current/μA", fontsize=14)

# Styling the plot
ax.spines["bottom"].set_position(("data", 0))
ax.spines["bottom"].set_color("black")
ax.spines["bottom"].set_linewidth(0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
ax.xaxis.set_label_coords(0.5, -0.05)
ax.tick_params(axis="both", which="major", labelsize=12)

# Add legend
ax.legend(['pH = 5.97', 'pH = 4.29', 'pH = 3.46', 'pH = 2.03'], fontsize=11)

# Save the plot
plt.savefig(SAVE_PATH / "CVs_part_B_pH.png", dpi=300, transparent=True)
plt.close()

### Calculate peak oxidation and reduction for the pH-altered system ###

def linear_extrapolation(x_vals, y_vals):
    """
    Perform linear extrapolation using the first-order polynomial fit.

    Args:
        x_vals (np.ndarray): Array of x values.
        y_vals (np.ndarray): Array of y values.

    Returns:
        np.ndarray: Coefficients of the linear fit (slope, intercept).
    """
    return np.polyfit(x_vals, y_vals, 1)

def find_ox_peak(df, coefs):
    """
    Find the oxidation peak by comparing the maximum current to the linear extrapolation.

    Args:
        df (pd.DataFrame): DataFrame with x and y data.
        coefs (np.ndarray): Coefficients from the linear fit.

    Returns:
        float: Difference between the observed and extrapolated maximum current.
    """
    y_max = df.iloc[1:, 1].max()
    x_max = df.iloc[df.iloc[1:, 1].idxmax(), 0]
    y_extrapolated = x_max * coefs[0] + coefs[1]
    return y_max - y_extrapolated

def find_red_peak(df, coefs):
    """
    Find the reduction peak by comparing the minimum current to the linear extrapolation.

    Args:
        df (pd.DataFrame): DataFrame with x and y data.
        coefs (np.ndarray): Coefficients from the linear fit.

    Returns:
        float: Difference between the observed and extrapolated minimum current.
    """
    y_min = df.iloc[1:, 1].min()
    x_min = df.iloc[df.iloc[1:, 1].idxmin(), 0]
    y_extrapolated = x_min * coefs[0] + coefs[1]
    return y_min - y_extrapolated

# Define regions for oxidation and reduction peaks
x_values_ox = np.array(df.iloc[1:21, 0], dtype=float)
y_values_ox = np.array(df.iloc[1:21, 1], dtype=float)
x_values_red = np.array(df.iloc[110:121, 0], dtype=float)
y_values_red = np.array(df.iloc[110:121, 1], dtype=float)

# Calculate oxidation and reduction peaks for each pH value
for key, df in df_dict.items():
    coefs_ox = linear_extrapolation(x_values_ox, y_values_ox)
    ox_peak = find_ox_peak(df.iloc[1:, 0:2], coefs_ox)

    coefs_red = linear_extrapolation(x_values_red, y_values_red)
    red_peak = find_red_peak(df.iloc[1:, 0:2], coefs_red)

    print(f"pH {key}: Oxidation Peak = {ox_peak:.3f}, Reduction Peak = {red_peak:.3f}")