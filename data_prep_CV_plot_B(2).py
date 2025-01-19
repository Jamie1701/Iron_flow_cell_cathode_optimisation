import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import os

folder_path = "/Users/jamiepersonal/Documents/Electrochemistry/Data/Part_B"

caesium_sulphate_file = "caesium_sulphate_3.xlsx"
lithium_sulphate_file = "lithium_sulphate_3.xlsx"
potassium_sulphate_file = "potassium_sulphate_3.xlsx"
sodium_sulphate_file = "sodium_sulphate_3.xlsx"

cs_path = os.path.join(folder_path, caesium_sulphate_file)
ls_path = os.path.join(folder_path, lithium_sulphate_file)
ps_path = os.path.join(folder_path, potassium_sulphate_file)
ss_path = os.path.join(folder_path, sodium_sulphate_file)

df_cs = pd.read_excel(cs_path, engine="openpyxl")
df_ls = pd.read_excel(ls_path, engine="openpyxl")
df_ps = pd.read_excel(ps_path, engine="openpyxl")
df_ss = pd.read_excel(ss_path, engine="openpyxl")

df_list = [df_cs, df_ls, df_ps, df_ss]

plt.rcParams['font.family'] = 'Times New Roman'  # Use Charter font
plt.rcParams['mathtext.fontset'] = 'stix' 

fig, ax = plt.subplots()

alpha_values = [0.3, 0.3, 1, 0.3]
color_values = ['blue', 'green', 'black', 'red']

for i, df in enumerate(df_list):
    ax.plot(df.iloc[1:,0], df.iloc[1:,1], alpha = alpha_values[i], color = color_values[i] )
    
ax.set_xlabel("Potential/V vs. Ag/AgCl", fontsize = 14)
ax.set_ylabel("Current/μA", fontsize = 14)
    
ax.spines['bottom'].set_position(('data', 0))
ax.spines['bottom'].set_color('black')
ax.spines['bottom'].set_linewidth(0.5)
    
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
    
ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    
ax.xaxis.set_label_coords(0.5,-0.05)
    
ax.legend([r'Cs$_2$SO$_4$', r'Li$_2$SO$_4$$\cdot$H$_2$O', r'K$_2$SO$_4$', r'Na$_2$SO$_4$$\cdot10$H$_2$O'],
          fontsize = 11,
          loc = "upper left")

ax.tick_params(axis='both', which='major', labelsize=12)
    
plt.savefig("/Users/jamiepersonal/Documents/Electrochemistry/Report/Graphs_2/CVs_part_B", dpi=300, transparent=True)
plt.close()