import pandas as pd

def load_data(file_path):
    """Load data from a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)

def unpivot_facility_metrics(df):
    """
    Unpivots a dataframe where the first column is 'Facility Name' and the rest are metrics.
    Returns a dataframe with columns: facility_name, metric_name, facility_metric_value.
    """
    df = df.rename(columns={df.columns[0]: "facility_name"})
    melted = df.melt(id_vars="facility_name", var_name="metric_name", value_name="facility_metric_value")
    return melted

def split_metric_name_columns(df):
    """
    Splits the 'metric_name' column into 'time_period', 'animal_description', and 'other_party'
    using newline (\n) as the delimiter. If there are fewer than three splits, fills with None.
    """
    splits = df['metric_name'].str.split('\n', n=2, expand=True)
    df['time_period'] = splits[0]
    df['animal_description'] = splits[1] if splits.shape[1] > 1 else None
    df['other_party'] = splits[2] if splits.shape[1] > 2 else None
    return df

def write_data(df, file_path):
    """Write the DataFrame to a CSV file."""
    # Always write all columns, including any new ones
    df.to_csv(file_path, index=False, columns=df.columns.tolist())

def split_animal_description(df):
    """
    Splits the 'animal_description' column into 'animal_age' and 'animal_type' using the first space.
    If no space is found, puts all data into 'animal_type' and sets 'animal_age' to an empty string.
    """
    def split_desc(desc):
        if pd.isna(desc):
            return '', ''
        desc = str(desc).strip()
        parts = desc.split(' ', 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return '', parts[0]
    df[['animal_age', 'animal_type']] = df['animal_description'].apply(lambda x: pd.Series(split_desc(x)))
    return df

if __name__ == "__main__":
    data = load_data("./Data/2023 Colorado Animal Shelter and Rescue Individual Report - Sheet1.csv")
    melty = unpivot_facility_metrics(data)
    columnar = split_metric_name_columns(melty)
    more_columns = split_animal_description(columnar)
    print(more_columns.head())
    write_data(more_columns, "./Data/columnar.csv")