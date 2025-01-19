import os
from pathlib import Path
import pandas as pd

# Root paths
ROOT_PATH = Path("/Users/jamiepersonal/Documents/Electrochemistry/Data")
PART_A1 = ROOT_PATH / "Part_A1"
PART_A2 = ROOT_PATH / "Part_A2"

def collect_files_by_prefix(directory, prefixes):
    """
    Collect files in a directory based on their prefixes and group them into a dictionary.
    
    Args:
        directory (Path): Path to the directory.
        prefixes (list): List of prefixes to search for.
    
    Returns:
        dict: Dictionary with prefixes as keys and sorted file lists as values.
    """
    file_dict = {prefix: [] for prefix in prefixes}
    try:
        for file in directory.iterdir():
            for prefix in prefixes:
                if file.name.startswith(prefix):
                    file_dict[prefix].append(file)
        # Sort file lists for consistency
        for prefix in file_dict:
            file_dict[prefix].sort()
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
    return file_dict

def load_excel_files(file_dict, engine="openpyxl"):
    """
    Load Excel files into pandas DataFrames based on a file dictionary.
    
    Args:
        file_dict (dict): Dictionary with keys as categories and values as file lists.
        engine (str): Engine for reading Excel files.
    
    Returns:
        dict: Dictionary with DataFrames for the first file in each category.
        dict: Dictionary with lists of DataFrames for all files in each category.
    """
    single_dfs = {}
    all_dfs = {}
    for key, files in file_dict.items():
        if files:
            try:
                single_dfs[key] = pd.read_excel(files[0], engine=engine)
                all_dfs[key] = [pd.read_excel(file, engine=engine) for file in files]
            except Exception as e:
                print(f"Error loading files for {key}: {e}")
    return single_dfs, all_dfs

# Part A1: File prefixes and data collection
A1_PREFIXES = ["ferrocene", "ferrocyanide", "iron"]
file_dict_A1 = collect_files_by_prefix(PART_A1, A1_PREFIXES)
df_dict_A1, df_dict_A1_full = load_excel_files(file_dict_A1)

# Part A2: File prefixes and data collection
A2_PREFIXES = ["ferrocene_DCM", "ferrocene_DMSO", "ferrocene_MeCN", "FCA_ferrocene", "FCA_MeCN"]
file_dict_A2 = collect_files_by_prefix(PART_A2, A2_PREFIXES)
df_dict_A2, df_dict_A2_full = load_excel_files(file_dict_A2)

# Change back to root directory
os.chdir(ROOT_PATH.parent)

# Print summaries for verification
print("Part A1 files loaded:")
print(df_dict_A1.keys())

print("\nPart A2 files loaded:")
print(df_dict_A2.keys())
