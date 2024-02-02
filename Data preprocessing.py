import pandas as pd

def remove_duplicates(input_file, output_file):
    # Assurez-vous que vous avez les bonnes colonnes dans les bons ordres comme dans votre fichier CSV
    df = pd.read_csv(input_file, header=None, names=["Name", "Visits", "Twitter", "Discord", "YouTube", "Roblox group"])
    # Supprime les doublons en se basant uniquement sur la colonne "Name"
    df_cleaned = df.drop_duplicates(subset=["Name"], keep='first')
    df_cleaned.to_csv(output_file, index=False, header=False)

remove_duplicates("social_links.csv", "clean_data.csv")
