import pandas as pd

def remove_duplicates(input_file, output_file):

    df = pd.read_csv(input_file, header=None, names=["Name", "Visits", "Twitter", "Discord", "YouTube", "Roblox group"])
    df = pd.read_csv(input_file, header=None, names=["Name", "Visits", "Twitter", "Discord", "YouTube", "Roblox group"])
    df_cleaned = df.drop_duplicates(subset=["Name"], keep='first')
    df_cleaned.to_csv(output_file, index=False, header=False)

remove_duplicates("social_links.csv", "clean_data.csv")
