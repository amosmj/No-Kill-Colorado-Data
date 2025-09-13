import utilities
if __name__ == "__main__":
    df = utilities.ingest_grid_data(r'/home/mikeamos/No-Kill-Colorado-Data/Data/2014 PACFA Data.xlsx')
    print(df.head())