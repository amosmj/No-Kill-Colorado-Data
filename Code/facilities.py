import pandas as pd

import utilities

def parse_pacfa_file(file_path, year):
    """
    Parses a PACFA file and returns a DataFrame with additional 'year' and 'year_part' columns.

    Parameters:
    file_path (str): The path to the PACFA data file.

    Returns:
    DataFrame: The parsed DataFrame with 'year' and 'year_part' columns.
    """
    df = utilities.ingest_grid_data(file_path)
    columns = df.columns
    expected_columns = ['Account Name', 'DBA', 'City', 'County', 'Business License App Category Name', 'Expire Date']
    for c in expected_columns:
        if c not in columns:
            raise ValueError(f"Expected column '{c}' not found in data.")
            df[c] = None
    df['Year'] = year

    return df

def read_local_pacfa_file(file_path: str):
    df = utilities.ingest_grid_data(file_path= file_path)
    return df

def add_pacfa_to_local_file(pacfa_df, year, path_to_local_file = r'Data/facilities.csv'):
    local_df = utilities.ingest_grid_data(path_to_local_file)
    df = utilities.ingest_grid_data(pacfa_df)
    columns = df.columns
    expected_columns = ['Account Name', 'DBA', 'City', 'County', 'Business License App Category Name', 'Expire Date']
    for c in expected_columns:
        if c not in columns:
            raise ValueError(f"Expected column '{c}' not found in data.")
            df[c] = None
    # delete year if it exists

    # write year
    

if __name__ == "__main__":
    pass