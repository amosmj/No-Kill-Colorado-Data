import utilities
import facilities
import interface
import year_file
import pandas as pd

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
    df = year_file.parse_year_file(year_data)
    df = year_file.update_facilities_csv(df, facilities_path="./Data/facilities.csv")
    return df

if __name__ == "__main__":
    # interface.run_streamlit_commands(port=8501, open_browser=True, timeout=10)
    # year_value, year_file_path, pacfa_data = interface.interface_for_annual_import()
    processes_year_df = year_file.parse_year_file(r'/Users/mike/Documents/GitHub/No-Kill-Colorado-Data/Data/2018 - Individual Animal Shelter and Rescue Report 8-8-19 Corrected.xlsx - Form Responses 1.csv')
    # pacfa_df = utilities.ingest_grid_data(pacfa_data)
    # year_int = int(year_value)