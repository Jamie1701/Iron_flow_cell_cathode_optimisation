import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from data_prep_2 import df_dict_A1_full, df_dict_A2_full

# Constants
ELECTRODE_AREA = 7.07e-6  # Electrode area in m^2 (3mm diameter)
FARADAY_CONSTANT = 2.69e5  # Faraday constant for diffusion calculations
SCAN_RATE_RANGES = {
    "ferrocyanide": slice(1, 8),  # Adjust as needed
    "ferrocene_DMSO": slice(1, 41),
    "ferrocene_methanol": slice(1, 9)
}

def extract_scan_rate(df):
    """Extract the scan rate from the DataFrame column header."""
    try:
        return df.columns[2]
    except IndexError:
        raise ValueError("Scan rate not found in column headers.")

def calculate_linear_fit(x_data, y_data):
    """Perform a linear fit and return the gradient and intercept."""
    x_data = np.array(x_data, dtype=float)
    y_data = np.array(y_data, dtype=float)
    return np.polyfit(x_data, y_data, 1)  # Returns [gradient, intercept]

def calculate_oxidation_peak(df, gradient_intercept):
    """
    Calculate the oxidation peak current by subtracting extrapolated baseline.
    
    Args:
        df (pd.DataFrame): Data for a single scan rate.
        gradient_intercept (tuple): Gradient and intercept of the baseline.
        
    Returns:
        float: Oxidation peak current.
    """
    y_max = df.iloc[1:, 1].max()
    x_max = df.iloc[df.iloc[1:, 1].idxmax(), 0]
    y_extrapolated = gradient_intercept[0] * x_max + gradient_intercept[1]
    return y_max - y_extrapolated

def process_species(df_list, scan_range, key):
    """
    Process data for a specific species to calculate oxidation peaks.
    
    Args:
        df_list (list): List of DataFrames for the species.
        scan_range (slice): Slice range for the linear region.
        key (str): Species key for logging purposes.
        
    Returns:
        dict: Oxidation peak currents for each scan rate.
    """
    x_data = {}
    y_data = {}
    grad_intercept = {}
    ox_peaks = {}
    
    for df in df_list:
        scan_rate = extract_scan_rate(df)
        x_data[scan_rate] = df.iloc[scan_range, 0]
        y_data[scan_rate] = df.iloc[scan_range, 1]
        grad_intercept[scan_rate] = calculate_linear_fit(x_data[scan_rate], y_data[scan_rate])
    
    for df in df_list:
        scan_rate = extract_scan_rate(df)
        ox_peaks[scan_rate] = calculate_oxidation_peak(df, grad_intercept[scan_rate])
    
    return ox_peaks

# Process data for ferrocyanide
ferrocyanide_dfs = df_dict_A1_full["ferrocyanide"]
ox_peak_ferrocyanide = process_species(ferrocyanide_dfs, SCAN_RATE_RANGES["ferrocyanide"], "ferrocyanide")

# Process data for ferrocene in DCM
ferrocene_DCM_dfs = df_dict_A2_full["ferrocene_DCM"]
ox_peak_DCM = {extract_scan_rate(df): df.iloc[1:, 1].max() for df in ferrocene_DCM_dfs}

# Process data for ferrocene in DMSO
ferrocene_DMSO_dfs = df_dict_A2_full["ferrocene_DMSO"]
ox_peak_DMSO = process_species(ferrocene_DMSO_dfs, SCAN_RATE_RANGES["ferrocene_DMSO"], "ferrocene_DMSO")

# Process data for ferrocene in MeCN
ferrocene_MeCN_dfs = df_dict_A2_full["ferrocene_MeCN"]
ox_peak_MeCN = {extract_scan_rate(df): df.iloc[1:, 1].max() for df in ferrocene_MeCN_dfs}

# Diffusion coefficient calculation
def calc_diffusion_from_gradient(ox_peak_dict):
    """
    Calculate diffusion coefficient from the gradient of oxidation peaks.
    
    Args:
        ox_peak_dict (dict): Oxidation peaks keyed by scan rates.
        
    Returns:
        tuple: Diffusion coefficient and gradient.
    """
    x_values = np.sqrt(np.array(list(ox_peak_dict.keys()), dtype=float))
    y_values = np.array(list(ox_peak_dict.values()), dtype=float) * 1e-6  # Convert μA to A
    gradient, _ = np.polyfit(x_values, y_values, 1)
    diffusion_coef = (gradient / (FARADAY_CONSTANT * ELECTRODE_AREA)) ** 2
    return diffusion_coef, gradient