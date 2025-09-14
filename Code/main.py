import utilities
import facilities
import parse_ind_state_file

def old_file_format(file_path):
    """
    Determines if the file at file_path is in the old format based on its extension.

    Parameters:
    file_path (str): The path to the data file.

    Returns:
    bool: True if the file is in the old format (.csv or .xlsx), False otherwise.
    """
    df = utilities.ingest_grid_data(file_path)

def new_file_format(year_data, facilities_data):
    """
    Processes year_data and facilities_data DataFrames.

    Parameters:
    year_data (DataFrame): The year data.
    facilities_data (DataFrame): The facilities data.

    Returns:
    DataFrame: Processed DataFrame.
    """
    df = parse_ind_state_file.parse_year_file(year_data)
    df = parse_ind_state_file.update_facilities_csv(df, facilities_path="./Data/facilities.csv")
    return df
if __name__ == "__main__":
    print("foo")