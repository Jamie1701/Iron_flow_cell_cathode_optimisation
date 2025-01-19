import matplotlib.pyplot as plt
import numpy as np
from ox_curr_root_scan_data import *
import os

# Constants
SAVE_PATH = "/Users/jamiepersonal/Documents/Electrochemistry/Report/Graphs_2/Peak_ox_vs_root_of_scan"
FONT_FAMILY = "Times New Roman"
MATH_FONTSET = "stix"

# Ensure the save path exists
os.makedirs(SAVE_PATH, exist_ok=True)

# Set Matplotlib parameters
plt.rcParams["font.family"] = FONT_FAMILY
plt.rcParams["mathtext.fontset"] = MATH_FONTSET

def prepare_data(scan_rates, peak_dict):
    """
    Prepare x (square root of scan rate) and y (oxidation peak current) values for plotting.

    Args:
        scan_rates (list or dict): Scan rates for the species.
        peak_dict (dict): Dictionary of peak currents keyed by scan rates.

    Returns:
        tuple: Arrays of x and y values for plotting.
    """
    x_values = [np.sqrt(rate) for rate in scan_rates]
    y_values = [peak_dict[rate] for rate in scan_rates]
    return np.array(sorted(x_values)), np.array(sorted(y_values))

def plot_peak_current_vs_scan_rate(x_values, y_values, label, filename):
    """
    Plot and save the peak current vs. square root of scan rate graph.

    Args:
        x_values (np.ndarray): Square root of scan rates.
        y_values (np.ndarray): Peak oxidation currents.
        label (str): Label for the graph (e.g., species name).
        filename (str): Name of the file to save the plot.
    """
    # Fit a linear regression line
    coefs = np.polyfit(x_values, y_values, 1)

    # Create the plot
    plt.figure()
    plt.plot(x_values, y_values, marker="o", linestyle="", label=label)
    plt.plot(x_values, coefs[0] * x_values + coefs[1], color="r", label="Linear fit")
    plt.xlabel(r"Square root of scan rate/$\left( V \, s^{-1} \right)^{\frac{1}{2}}$", fontsize=15)
    plt.ylabel("Peak oxidation current/μA", fontsize=15)
    plt.ylim(0,)
    plt.xlim(0,)
    plt.tick_params(axis="both", which="major", labelsize=11)
    plt.legend(fontsize=12)
    plt.tight_layout()

    # Save the plot
    plt.savefig(os.path.join(SAVE_PATH, filename), dpi=300, transparent=True)
    plt.close()

# Prepare data and plot for each species

# Ferrocyanide
x_values, y_values = prepare_data(scan_rate_1, ox_peak_dict_ferrocyanide)
plot_peak_current_vs_scan_rate(x_values, y_values, "Ferrocyanide", "ferrocyanide.png")

# Ferrocene in DCM
x_values, y_values = prepare_data(scan_rate_2_3_4["ferrocene_DCM"], ox_peak_dict_DCM)
plot_peak_current_vs_scan_rate(x_values, y_values, "Ferrocene (DCM)", "DCM.png")

# Ferrocene in DMSO
x_values, y_values = prepare_data(scan_rate_2_3_4["ferrocene_DMSO"], ox_peak_dict_DMSO)
plot_peak_current_vs_scan_rate(x_values, y_values, "Ferrocene (DMSO)", "DMSO.png")

# Ferrocene in MeCN
x_values, y_values = prepare_data(scan_rate_2_3_4["ferrocene_MeCN"], ox_peak_dict_MeCN)
plot_peak_current_vs_scan_rate(x_values, y_values, "Ferrocene (MeCN)", "MeCN.png")