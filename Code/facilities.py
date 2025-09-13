import utilities


if __name__ == "__main__":
    df = utilities.ingest_grid_data(r'./Data/Copy of Active PACFA List - Active List.csv')
    print(df.head())
    print(df.shape)