from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
username_field.send_keys('0xUnpeg')
password_field = driver.find_element(By.ID, 'login-password')
password_field.send_keys('Flavien2002')
password_field.send_keys(Keys.RETURN)
sleep(5)

visited_games = set()

def get_social_links_and_save(game_name):
    links = {'Game Name': game_name, 'Twitter': '', 'Discord': '', 'YouTube': ''}
    social_links = driver.find_elements(By.XPATH, '//div[@id="social-link-card"]//a[@class="social-link"]')
    for link in social_links:
        url = link.get_attribute('href')
        title = link.get_attribute('title')
        if 'twitter.com' in url:
            links['Twitter'] = url
        elif 'discord.gg' in url:
            links['Discord'] = url
        elif 'youtube.com' in url:
            links['YouTube'] = url

    with open('social_links.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=links.keys())
        if file.tell() == 0:  # Si le fichier est vide, écrire l'en-tête
            writer.writeheader()
        writer.writerow(links)
    print(f"Social links found and saved for {game_name}")

def get_recommended_games():
    game_links = []
    game_cards = driver.find_elements(By.XPATH, '//div[@data-testid="game-tile"]')
    for card in game_cards:
        player_count_element = card.find_element(By.XPATH, './/span[@class="info-label playing-counts-label"]')
        player_count_text = player_count_element.text.replace('K', '000')
        player_count = int(re.sub("[^0-9]", "", player_count_text))

        if 10 <= player_count <= 1500:
            game_link = card.find_element(By.XPATH, './/a[@class="game-card-link"]')
            game_links.append(game_link.get_attribute('href'))
    return game_links

def process_game(game_url):
    global visited_games
    sleep(random.uniform(2.3, 8.38))
    driver.get(game_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="game-name-title"]'))
        )
        game_name_element = driver.find_element(By.XPATH, '//div[@class="game-name-title"]')
        game_name = game_name_element.text
    except NoSuchElementException:
        game_name = "Unknown Game"

    get_social_links_and_save(game_name)

    visited_games.add(game_url)
    print(f"Processing game: {game_name}")

    recommended_games = get_recommended_games()
    for recommended_game_url in recommended_games:
        if recommended_game_url not in visited_games:
            print(f"Found new game to visit")
            return recommended_game_url

    print("No more unique recommended games")
    return None

def get_all_game_urls():
    driver.get('https://www.roblox.com/discover#/sortName/Curated_103')
    sleep(5)
    game_elements = driver.find_elements(By.CLASS_NAME, "game-card-link")
    return [element.get_attribute('href') for element in game_elements]

# --- CHANGE THE INDEX VALUE TO RESUME FROM A SPECIFIC POINT ---

start_index = 44

all_game_urls = get_all_game_urls()

for i, game_url in enumerate(all_game_urls):
    if i >= start_index:
        current_game_url = game_url
        while current_game_url is not None:
            current_game_url = process_game(current_game_url)
            if current_game_url is None:
                print("Switching to the next game 🎲")

driver.quit()
