def ingest_grid_data(file_path):
    """
    Ingest data from a specified file path.

    Parameters:
    file_path (str): The path to the data file.

    Returns:
    data: The ingested data.
    """
    if file_path.endswith('.csv'):
        import pandas as pd
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        import pandas as pd
        data = pd.read_excel(file_path)
    else:
        data = pd.DataFrame()
    return data



def write_data(df, file_path):
    """Write the DataFrame to a CSV file."""
    # Always write all columns, including any new ones
    df.to_csv(file_path, index=False, columns=df.columns.tolist())