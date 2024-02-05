from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re
from time import sleep
import csv
import random

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)




# --- LOGIN INTO ROBLOX ---

driver.get('https://www.roblox.com/login')
username_field = driver.find_element(By.ID, 'login-username')
username_field.send_keys('Enter your Roblox username')
password_field = driver.find_element(By.ID, 'login-password')
password_field.send_keys('Enter your Roblox password')
password_field.send_keys(Keys.RETURN)
sleep(5)

visited_games = set()

def get_game_name():
    try:
        game_name_element = driver.find_element(By.XPATH, '//h1[contains(@class, "game-name")]')
        game_name = game_name_element.text.strip()
        print(f"Game name found: {game_name}")
        return game_name
    except NoSuchElementException:
        print("Game name not found")
        return "Unknown Game"

def get_game_visits():
    try:
        visits_element = driver.find_element(By.ID, 'game-visit-count')
        visits = visits_element.get_attribute('title').strip()
        print(f"Game visits found: {visits}")
        return visits
    except NoSuchElementException:
        print("Game visits not found")
        return "Unknown"

def get_social_links_and_save():
    game_name = get_game_name()  # Extract the game name
    game_visits = get_game_visits()  # Extract the game visits
    twitter_link = ""
    discord_link = ""
    youtube_link = ""
    roblox_group_link = ""
    try:
        twitter_element = driver.find_element(By.XPATH, '//a[contains(@class, "social-link")][contains(@href, "twitter.com")]')
        twitter_link = twitter_element.get_attribute('href')
        print(f"Twitter link found 🐦 : ✅")
    except NoSuchElementException:
        print("No Twitter link found 🐦 : ❌")

    try:
        discord_element = driver.find_element(By.XPATH, '//a[contains(@class, "social-link")][contains(@href, "discord.gg")]')
        discord_link = discord_element.get_attribute('href')
        print(f"Discord link found 👾 : ✅")
    except NoSuchElementException:
        print("No Discord link found 👾 : ❌")

    try:
        youtube_element = driver.find_element(By.XPATH, '//a[contains(@class, "social-link")][contains(@href, "youtube.com")]')
        youtube_link = youtube_element.get_attribute('href')
        print(f"Discord link found 🍄 : ✅")
    except NoSuchElementException:
        print("No Discord link found 👾 : ❌")

    try:
        roblox_group_element = driver.find_element(By.XPATH, '//a[contains(@class, "social-link")][contains(@href, "roblox.com")]')
        roblox_group_link = roblox_group_element.get_attribute('href')
        print(f"Roblox group link found 🦸‍♂️ : ✅")
    except NoSuchElementException:
        print("No Roblox group link found 🦸‍♂️ : ❌")

    if twitter_link or discord_link or roblox_group_link:
        with open('social_links.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Include game name and visits in the CSV
            writer.writerow([game_name, game_visits, twitter_link, discord_link, youtube_link, roblox_group_link])

def get_recommended_games():
    game_links = []
    game_cards = driver.find_elements(By.XPATH, '//div[@data-testid="game-tile"]')
    for card in game_cards:
        player_count_element = card.find_element(By.XPATH, './/span[@class="info-label playing-counts-label"]')
        player_count_text = player_count_element.text.replace('K', '000')
        player_count = int(re.sub("[^0-9]", "", player_count_text))

        if 0 <= player_count <= 100000:
            game_link = card.find_element(By.XPATH, './/a[@class="game-card-link"]')
            game_links.append(game_link.get_attribute('href'))
    return game_links

def process_game(game_url):
    global visited_games
    sleep(random.uniform(1.1, 1.78))
    driver.get(game_url)
    sleep(random.uniform(1.2, 1.91))
    get_social_links_and_save()
    visited_games.add(game_url)


    recommended_games = get_recommended_games()
    for recommended_game_url in recommended_games:
        if recommended_game_url not in visited_games:
            print(f"Found new game to visit 🌟")
            return recommended_game_url

    print("No more unique recommended games")
    return None

def get_all_game_urls():
    driver.get('https://www.roblox.com/discover#/sortName/TopGrossing')
    sleep(random.uniform(1.8, 1.9))  # Adjust sleep time for page load
    game_elements = driver.find_elements(By.CLASS_NAME, "game-card-link")
    return [element.get_attribute('href') for element in game_elements]

# --- CHANGE THE INDEX VALUE TO RESUME FROM A SPECIFIC GAME ON THE PAGE ---

start_index = 5

all_game_urls = get_all_game_urls()

for i, game_url in enumerate(all_game_urls):
    if i >= start_index:
        current_game_url = game_url
        while current_game_url is not None:
            current_game_url = process_game(current_game_url)
            if current_game_url is None:
                print("Switching to the next game 🎲")

driver.quit()
