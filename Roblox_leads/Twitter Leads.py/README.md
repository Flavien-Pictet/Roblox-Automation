_____________________________________TL/DR_______________________________________


The goal of this bot is to scrape Twitter profile links within Roblox using specific filters to generate relevant leads.

The file "Data preprocessing.py" is designed to automatically eliminate duplicates and produce a clean dataset.

How does the bot work?

The bot scrapes the Roblox "Discover" page sections such as "Recommended for you" or "Over 17 games", analyzes each game to determine if there is an associated Twitter link to retrieve. Every game has 6 recommended games when you scroll down; the bot will analyze each of them to check if they meet our criteria and will repeat the process continually until no new games are left to scrape.

When the bot stops, you will need to modify the link at line 73 and begin scraping a new page. Repeat this process as necessary.

__________________________________________________________________________________
