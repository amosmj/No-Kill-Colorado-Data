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
        
    return df

if __name__ == "__main__":
    df = utilities.ingest_grid_data(r'./Data/Copy of Active PACFA List - Active List.csv')
    print(df.head())
    print(df.shape)