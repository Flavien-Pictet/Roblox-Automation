import pandas as pd

twitter_links = pd.read_csv('twitter_links.csv', header=None)
twitter_links = twitter_links.drop_duplicates()
twitter_links.to_csv('clean_links.csv', index=False, header=False)
