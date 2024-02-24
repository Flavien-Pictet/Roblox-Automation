import threading
import httpx
import time

cookie = '...'
cookie_session = httpx.Client()
cookie_session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Cookie': f'.ROBLOSECURITY={cookie}'
}

class database:
    games = []
    ids = []
    scraped = {}

with open('/Users/Flavien.PICTET/Automation /Roblox_leads/Twitter Leads.py/games.csv', 'r', encoding='utf-8') as f:
    database.games = f.read().splitlines()[1:]
    [database.ids.append(int(game.split(',')[-2])) for game in database.games[1:]]

print(f'Loaded {len(database.games)} games from data.csv!')

def update_games():
    with open('/Users/Flavien.PICTET/Automation /Roblox_leads/Twitter Leads.py/games.csv', 'w', encoding='utf-8') as f:
        header = 'Name, Visits, Twitter, Discord, YouTube, Roblox group'
        games = '\n'.join(database.games)
        data = f'{header}\n{games}'
        f.write(data + '\n')

session = httpx.Client()
session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

response = session.get('https://games.roblox.com/v1/games/sorts?gameSortsContext=GamesDefaultSorts')
sort_token = [sort for sort in response.json()['sorts'] if sort['name'] == 'TopGrossing'][0]['token']

start_rows = 0
while True:
    response = session.get(f'https://games.roblox.com/v1/games/list?sortToken={sort_token}&startRows={start_rows}&maxRows=200')
    for game in response.json()['games']:
        start_rows += 1
        player_count = game['playerCount']
        if player_count >= 1 and player_count <= 100000:
            place_id = game['placeId']
            name = game['name']
            creator_id = game['creatorId']
            creator_type = game['creatorType']
            if creator_type == 'User':
                creator_url = f'https://www.roblox.com/users/{creator_id}/profile'
            elif creator_type == 'Group':
                creator_url = f'https://www.roblox.com/groups/{creator_id}'
            universe_id = game['universeId']
            if place_id not in database.ids:
                database.scraped[place_id] = {
                    'name': name,
                    'creator_type': creator_type,
                    'creator_url': creator_url,
                    'universe_id': universe_id
                }
    has_more_games = response.json()['hasMoreRows']
    if not has_more_games:
        break
    time.sleep(1)

print(f'Scraped {len(database.scraped.keys())} top grossing games!')

def recommendations():
    counter = 0
    while True:
        try:
            time.sleep(30)
            if (counter + 1) > len(database.ids):
                continue
            universe_id = database.games[counter].split(',')[-1]
            response = session.get(f'https://games.roblox.com/v1/games/recommendations/game/{universe_id}')
            for game in response.json()['games']:
                player_count = game['playerCount']
                if player_count >= 1 and player_count <= 100000:
                    place_id = game['placeId']
                    name = game['name']
                    creator_id = game['creatorId']
                    creator_type = game['creatorType']
                    if creator_type == 'User':
                        creator_url = f'https://www.roblox.com/users/{creator_id}/profile'
                    elif creator_type == 'Group':
                        creator_url = f'https://www.roblox.com/groups/{creator_id}'
                    universe_id = game['universeId']
                    if place_id not in database.ids:
                        database.scraped[place_id] = {
                            'name': name,
                            'creator_type': creator_type,
                            'creator_url': creator_url,
                            'universe_id': universe_id
                        }
            counter += 1
            print(f'Scraped recommendations from game #{counter}! There are now {len(database.scraped.keys())} games in the queue.')
        except:
            print('An unknown error has occured while attempting to scrape game recommendations! Sleeping for 10 minutes to avoid rate limits...')
            time.sleep(600)

threading.Thread(target=recommendations).start()

while True:
    time.sleep(5)
    if database.scraped:
        try:
            place_id = list(database.scraped.keys())[0]
            print(f'Scraping new game: {place_id}')
            game = database.scraped[place_id]
            name = game['name']
            creator_type = game['creator_type']
            creator_url = game['creator_url']
            universe_id = game['universe_id']
            visits = '{:,}'.format(httpx.get(f'https://games.roblox.com/v1/games?universeIds={universe_id}').json()['data'][0]['visits']).replace(',', ' ')
            twitter = 'N/A'
            discord = 'N/A'
            youtube = 'N/A'
            group = 'N/A'
            response = cookie_session.get(f'https://games.roblox.com/v1/games/{universe_id}/social-links/list')
            for social in response.json()['data']:
                social_url = social['url']
                social_type = social['type']
                if social_type == 'Twitter':
                    twitter = social_url
                elif social_type == 'Discord':
                    discord = social_url
                elif social_type == 'YouTube':
                    youtube = social_url
                elif social_type == 'RobloxGroup':
                    group = social_url
            if group == 'N/A' and creator_type == 'Group':
                group = creator_url
            database.games.append(f'{name},{visits},{twitter},{discord},{youtube},{group},{place_id},{universe_id}')
            database.ids.append(place_id)
            del database.scraped[place_id]
            update_games()
        except:
            print('An unknown error has occured while attempting to scrape the game! Sleeping for 10 minutes to avoid rate limits...')
            time.sleep(600)
