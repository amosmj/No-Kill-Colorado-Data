import utilities
import facilities
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
    # big_sheet_df = utilities.ingest_grid_data(file_path='/home/mikeamos/No-Kill-Colorado-Data/Data/Colorado Animal Shelter and Rescue Individual Report .xlsx', sheet_name='2024')
    # # print(big_sheet_df.head())
    # print(big_sheet_df.columns)
    # # little_sheet_df = utilities.ingest_grid_data(file_path='/home/mikeamos/No-Kill-Colorado-Data/Data/No-Kill-Colorado-Data.csv')
    # # print(little_sheet_df.head())
    # # print(little_sheet_df.columns)
    # facilites_df = facilities.parse_pacfa_file(r'./Data/Copy of Active PACFA List - Active List.csv',2024)
    # print(facilites_df.columns)

    # df1 = pd.merge(big_sheet_df,facilites_df,how='inner', left_on= 'Facility Name', right_on='Account Name')
    # # print(df1['Facility Name'].unique())

    # df2 = pd.merge(big_sheet_df,facilites_df,how='inner', left_on= 'Facility Name', right_on='DBA')
    # # print(df2['Facility Name'].unique())

    # account_name_join_count = 0
    # for fac in df1['Facility Name'].unique():
    #     if fac in df2['Facility Name'].unique():
    #         account_name_join_count =account_name_join_count + 1

    # unique_values_on_acct_name = len(df1['Facility Name'].unique())
    # print(f"There are {unique_values_on_acct_name} values when joining on Account Name {account_name_join_count} are found in th list found on DBA")

    # dba_join_count = 0
    # for fac in df2['Facility Name'].unique():
    #     if fac in df1['Facility Name'].unique():
    #         dba_join_count +=1

    # unique_values_in_dba = len(df2['Facility Name'].unique())
    # print(f"There are {unique_values_in_dba} values when I join on DBA, {dba_join_count} are found in  the Facility Name join.")

    # join_of_join = pd.merge(df1, df2, how='inner', on='Facility Name',indicator=True)
    # check_this_list = join_of_join['Facility Name'].unique()

    # print(facilites_df.columns)
    # for fac in check_this_list:
    #     print("Checking", fac)
    #     print(facilites_df[facilites_df['Account Name']==fac])
    #     print(facilites_df[facilites_df['DBA']==fac])
    pass