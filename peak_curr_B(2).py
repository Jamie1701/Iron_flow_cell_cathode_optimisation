from data_prep_CV_plot_B import *
import numpy as np
import pandas as pd

x_values_ps = np.array(df_ps.iloc[1:21,0], dtype=float)
y_values_ps = np.array(df_ps.iloc[1:21,1], dtype=float)

x_values_ps_red = np.array(df_ps.iloc[105:121,0], dtype=float)
y_values_ps_red = np.array(df_ps.iloc[105:121,1], dtype=float)

def linear_extrapolation(x_vals, y_vals):
    coefs = np.polyfit(x_vals, y_vals, 1)
    return coefs

def find_ox_peak(df,coefs):
    
    y_max = df.iloc[1:,1].max()
    x_max = df.iloc[df.iloc[1:,1].idxmax(),0]
    
    y_extrapolated = x_max*coefs[0] + coefs[1]
    
    return y_max - y_extrapolated

def find_red_peak(df,coefs):
    
    y_min = df.iloc[1:,1].min()
    x_min = df.iloc[df.iloc[1:,1].idxmin(),0]
    
    y_extrapolated = x_min*coefs[0] + coefs[1]
    
    return y_min - y_extrapolated
    
print(find_ox_peak(df_ps.iloc[1:,0:2], coefs=linear_extrapolation(x_values_ps,y_values_ps)), 
      find_red_peak(df_ps.iloc[1:,0:2], coefs=linear_extrapolation(x_values_ps_red,y_values_ps_red)) )
    