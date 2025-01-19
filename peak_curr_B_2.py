from data_prep_CV_plot_B_2 import df_ps  
import numpy as np
import pandas as pd

x_values_ps = np.array(df_ps.iloc[1:21, 0], dtype=float)
y_values_ps = np.array(df_ps.iloc[1:21, 1], dtype=float)

x_values_ps_red = np.array(df_ps.iloc[105:121, 0], dtype=float)
y_values_ps_red = np.array(df_ps.iloc[105:121, 1], dtype=float)

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

ox_peak = find_ox_peak(df_ps.iloc[1:, 0:2], coefs=linear_extrapolation(x_values_ps, y_values_ps))
red_peak = find_red_peak(df_ps.iloc[1:, 0:2], coefs=linear_extrapolation(x_values_ps_red, y_values_ps_red))