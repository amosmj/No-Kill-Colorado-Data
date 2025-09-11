import pandas as pd



file_name = r'Data/2023 Colorado Animal Shelter and Rescue Individual Report - Sheet1.csv'
with open(file_name,'r') as f:
    file = f.read()

df = pd.read_csv(file_name)


# print(data_dict)