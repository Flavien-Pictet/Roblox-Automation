import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

driver = webdriver.Chrome()
driver.get('https://www.roblox.com/login')

username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-username')))
password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))

username_field.send_keys('Enter your Roblox username')
password_field.send_keys('Enter your password')

login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-button')))
login_button.click()

time.sleep(3)

driver.get('Enter the Roblox community link')

time.sleep(3)

profile_links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.text-name')))

group_url = 'Enter the Roblox community link'

i = 0

while True:
    profile_links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.text-name')))
    if not profile_links:
        print("No more profiles to send friend requests to, you Sybilled everyone...")
        break

    for profile_link in profile_links[i:]:
        try:
            user_profile_url = profile_link.get_attribute('href')
            driver.execute_script(f"window.open('{user_profile_url}', 'new_tab')")
            driver.switch_to.window('new_tab')

            time.sleep(random.uniform(3, 12.8))
            try:
                add_friend_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'btn-control-md'))
                )
                add_friend_button.click()

                time.sleep(random.uniform(5, 14.5))
                print("Friend request sent to user.")
            except Exception as e:
                print(f"Couldn't find add friend button: {e}")
            finally:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(f"Couldn't navigate to profile: {e}")

        i += 1

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(random.uniform(2.5, 5.9))
    if driver.current_url != group_url:
        driver.get(group_url)
        time.sleep(2)
