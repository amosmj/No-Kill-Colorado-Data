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