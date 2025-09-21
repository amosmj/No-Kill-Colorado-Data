import pandas as pd

def ingest_grid_data(file_path, sheet_name=0):
    """
    Ingest data from a specified file path.

    Parameters:
    file_path (str): The path to the data file.

    Returns:
    data: The ingested data.
    """
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path, dtype=str)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path, dtype=str, sheet_name= sheet_name)
    else:
        data = pd.DataFrame()
    return data
