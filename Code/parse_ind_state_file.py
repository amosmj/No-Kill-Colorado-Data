import os
import pandas as pd

"""Expects file from : https://ag.colorado.gov/animal-welfare/pet-animal-care-facilities-act-pacfa/animal-shelter-and-rescue-individual-statistics"""

def update_no_kill_colorado_data(df, output_path="./Data/No-Kill-Colorado-Data.csv"):
    """
    Updates No-Kill-Colorado-Data.csv with new data for a given year, removing any existing data for that year.
    Appends new data, sorts, and overwrites the file.
    """
    import numpy as np
    import os
    columns = [
        "facility_name", "other_party", "year", "year_part", "animal_age", "animal_type", "facility_metric_value"
    ]
    # Read existing data if file exists
    if os.path.exists(output_path):
        existing_df = pd.read_csv(output_path)
    else:
        existing_df = pd.DataFrame(columns=columns)

    # Get the year from the new data (expect only one)
    years = df["year"].dropna().unique()
    if len(years) == 1:
        year = years[0]
        # Remove any rows from existing_df with this year
        existing_df = existing_df[existing_df["year"] != year]

    # Assemble new data with required columns
    new_df = df.copy()
    # Ensure all required columns exist
    for col in columns:
        if col not in new_df.columns:
            new_df[col] = ""
    new_df = new_df[columns]

    # Append and sort
    combined = pd.concat([existing_df, new_df], ignore_index=True)
    combined = combined.sort_values(by=["year", "year_part", "animal_type", "animal_age", "other_party", "facility_name"])
    combined.to_csv(output_path, index=False)
    return combined


def check_animal_synonym(df, synonyms_path="./Data/synonyms.csv"):
    """
    Standardizes values in animal_type, animal_age, or other_party columns using synonyms.csv.
    If synonyms.csv does not exist, creates an empty one with columns: column_name, desired_value, synonym_value.
    Replaces any value in the specified column that matches synonym_value (case-insensitive) with desired_value.
    """
    columns = ["animal_description", "desired_age", "desired_animal"]
    if os.path.exists(synonyms_path):
        syn_df = pd.read_csv(synonyms_path)
    else:
        syn_df = pd.DataFrame(columns=columns)
        syn_df.to_csv(synonyms_path, index=False)

    df["animal_description_match"] = df["animal_description"].str.strip().str.lower()
    syn_df["animal_description_match"] = syn_df["animal_description"].str.strip().str.lower()
    merged_df = pd.merge(df, syn_df, how='left', left_on='animal_description_match', right_on='animal_description_match', suffixes=('', '_syn'), indicator=True)
    # Clean up merged_df as requested
    cleaned = merged_df.copy()
    cleaned["animal_age"] = cleaned.apply(
        lambda row: row["desired_age"] if row["_merge"] == "both" and pd.notnull(row["desired_age"]) else row["animal_age"], axis=1
    )
    cleaned["animal_type"] = cleaned.apply(
        lambda row: row["desired_animal"] if row["_merge"] == "both" and pd.notnull(row["desired_animal"]) else row["animal_type"], axis=1
    )
    out_cols = ["facility_name", "other_party", "facility_metric_value", "year", "year_part", "animal_age", "animal_type"]
    out_cols = [col for col in out_cols if col in cleaned.columns]
    result = cleaned[out_cols]
    return result


def extract_year_and_part(df):
    """
    Adds 'year' and 'year_part' columns based on 'time_period'.
    - If time_period is 4 digits, year = time_period, year_part = 'during'.
    - If time_period is a date (MM/DD/YYYY), year = YYYY, year_part = 'beginning' if month is 1 or 01, 'end' if month is 12, else 'during'.
    """
    def parse_period(tp):
        if pd.isna(tp):
            return '', ''
        tp = str(tp).strip()
        if len(tp) == 4 and tp.isdigit():
            return tp, 'during'
        # Try to parse as MM/DD/YYYY
        try:
            parts = tp.split('/')
            if len(parts) == 3:
                month = parts[0].zfill(2)
                year = parts[2][-4:]
                if month in ['1', '01']:
                    return year, 'beginning'
                elif month == '12':
                    return year, 'end'
                else:
                    return year, 'during'
        except Exception:
            pass
        return '', ''
    df[['year', 'year_part']] = df['time_period'].apply(lambda x: pd.Series(parse_period(x)))
    return df


def update_facilities_csv(df, facilities_path="./Data/facilities.csv"):
    """
    Ensures all unique facility names in df['facility_name'] are present in facilities.csv (name or synonyms).
    If facilities.csv does not exist, creates it with required columns.
    Adds missing facilities to the end and overwrites the file.
    Returns the updated facilities DataFrame.
    """
    columns = ["name", "synonyms", "street_address", "city", "state", "zip", "long", "lat"]
    if os.path.exists(facilities_path):
        facilities_df = pd.read_csv(facilities_path)
    else:
        facilities_df = pd.DataFrame(columns=columns)

    # Ensure all required columns exist
    for col in columns:
        if col not in facilities_df.columns:
            facilities_df[col] = ""

    # Get unique facility names from input df
    unique_names = set(df["facility_name"].unique())
    # Remove names that are empty or only whitespace
    unique_names = {name for name in unique_names if isinstance(name, str) and name.strip()}
    # Get names and synonyms from facilities_df
    existing_names = set(facilities_df["name"].dropna().astype(str))
    # Synonyms may be comma-separated lists
    existing_synonyms = set()
    if "synonyms" in facilities_df.columns:
        for syns in facilities_df["synonyms"].dropna():
            for s in str(syns).split(","):
                s = s.strip()
                if s:
                    existing_synonyms.add(s)

    # Add missing facilities
    for name in unique_names:
        if name not in existing_names and name not in existing_synonyms:
            # Skip names that are empty or only whitespace (extra guard)
            if not isinstance(name, str) or not name.strip():
                continue
            new_row = {col: "" for col in columns}
            new_row["name"] = name
            facilities_df = pd.concat([facilities_df, pd.DataFrame([new_row])], ignore_index=True)

    # Overwrite the file
    facilities_df.to_csv(facilities_path, index=False)
    return None


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
    all_things_parsed = extract_year_and_part(more_columns)
    update_facilities_csv(more_columns)
    synonymed = check_animal_synonym(all_things_parsed)
    update_no_kill_colorado_data(synonymed)
    write_data(all_things_parsed, "./Data/No-Kill-Colorado-Data.csv")