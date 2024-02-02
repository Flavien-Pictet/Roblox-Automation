import time
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

driver.get('https://www.roblox.com/discover#/sortName/TopGrossing')
time.sleep(3)  # Attendre que la page initiale charge

def scroll_and_load_content(scroll_increment=1000, max_scroll_limit=10000):
    last_height = driver.execute_script("return document.body.scrollHeight")
    total_scrolled = 0

    while total_scrolled < max_scroll_limit:
        # Faire défiler de scroll_increment
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        total_scrolled += scroll_increment
        time.sleep(1)  # Laisser le temps pour le chargement du contenu

        # Vérifier la nouvelle hauteur après le chargement
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Arrêter si la hauteur n'a pas changé, indiquant la fin du contenu
        last_height = new_height

# Exemple d'utilisation
scroll_and_load_content()

# Après le défilement, vous pouvez ajouter des vérifications ici pour voir si de nouveaux jeux ont été chargés
# Par exemple, compter le nombre d'éléments correspondant aux jeux
games_loaded = len(driver.find_elements_by_xpath('//div[@data-testid="game-tile"]'))
print(f"Nombre de jeux chargés : {games_loaded}")

driver.quit()
