import pandas as pd

def remove_duplicates(input_file, output_file):
    df = pd.read_csv(input_file, header=None, names=["Twitter", "Discord"])
    df_cleaned = df.drop_duplicates()
    df_cleaned.to_csv(output_file, index=False, header=False)

remove_duplicates("social_links.csv", "clean_social_links.csv")
