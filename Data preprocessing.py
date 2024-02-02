import pandas as pd

# Lire le fichier CSV d'entrée
input_csv_file = "twitter_links.csv"
df = pd.read_csv(input_csv_file, header=None, names=["data"])  # Remplacez "data" par le nom de la colonne que vous souhaitez dédupliquer

# Supprimer les doublons
df_cleaned = df.drop_duplicates(subset=["data"])  # Remplacez "data" par le nom de la colonne que vous souhaitez dédupliquer

# Enregistrer les données nettoyées dans un nouveau fichier CSV
output_csv_file = "clean_data.csv"
df_cleaned.to_csv(output_csv_file, index=False, header=False)

print(f"Données nettoyées enregistrées dans '{output_csv_file}'.")
