from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json
import time
import random
import os
import pickle
from fake_useragent import UserAgent
from datetime import datetime

# Configuration
SITE_URL = "https://www.leboncoin.fr/"
OUTPUT_FILE = "scraped_data.json"
DRIVER_PATH = r"E:\RustNetwork\project\src\scrap_py\pro\msedgedriver.exe"  # Chemin vers msedgedriver.exe
EDGE_PROFILE_PATH = r"C:\Users\juankroos\AppData\Local\Microsoft\Edge\User Data"  # Profil Edge
COOKIES_PATH = "cookies.pkl"
PROXY_LIST = [
    "http://user:pass@ip1:port",  # Remplacez par vos proxys
    "http://user:pass@ip2:port",
]  # Liste d'exemple, fournissez vos proxys

# Initialiser User Agent
ua = UserAgent()

# Initialiser le navigateur (Microsoft Edge)
options = Options()
options.add_argument("--start-maximized")
options.add_argument(f"user-data-dir={EDGE_PROFILE_PATH}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-notifications")
options.add_argument(f"user-agent={ua.random}")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
#options.add_argument(f"--proxy-server={random.choice(PROXY_LIST)}")  # Rotation d'IP

service = Service(DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)

# Masquer navigator.webdriver et autres indicateurs
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        window.chrome = { runtime: {} };
    """
})

def human_mouse_move(driver, element):
    """Simule un mouvement de souris humain."""
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(element, random.randint(-5, 5), random.randint(-5, 5))
    actions.pause(random.uniform(0.5, 2.0))
    actions.click()
    actions.perform()

def human_scroll(driver, pixels=500):
    """Simule un défilement humain."""
    driver.execute_script(f"window.scrollBy(0, {pixels});")
    time.sleep(random.uniform(1.0, 2.0))

def save_cookies(driver, path=COOKIES_PATH):
    """Sauvegarde les cookies."""
    with open(path, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print(f"Cookies sauvegardés dans {path}")

def load_cookies(driver, path=COOKIES_PATH):
    """Charge les cookies."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print(f"Cookies chargés depuis {path}")
    else:
        print("Aucun fichier de cookies trouvé.")

def scrape_leboncoin():
    """Scrape les titres et prix après une recherche."""
    try:
        # Charger les cookies
        driver.get(SITE_URL)
        load_cookies(driver)
        driver.get(SITE_URL)  # Recharger pour appliquer les cookies
        time.sleep(random.uniform(2.0, 4.0))  # Simuler un temps de lecture

        # Trouver la barre de recherche
        search_bar = driver.find_element(By.XPATH, "//input[@placeholder='Que recherchez-vous ?']")
        human_mouse_move(driver, search_bar)
        time.sleep(random.uniform(0.5, 1.5))

        # Saisir la recherche
        search_query = "vélo"
        for char in search_query:
            search_bar.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Simuler une frappe humaine
        time.sleep(random.uniform(1.0, 2.0))

        # Cliquer sur le bouton de recherche
        search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        human_mouse_move(driver, search_button)
        time.sleep(random.uniform(2.0, 4.0))

        # Sauvegarder les cookies après interaction
        save_cookies(driver)

        # Faire défiler la page des résultats
        for _ in range(3):  # Défilement progressif
            human_scroll(driver, pixels=random.randint(300, 600))

        # Extraire les annonces
        listings = driver.find_elements(By.XPATH, "//a[@data-qa-id='aditem_container']")
        results = []
        for listing in listings:
            try:
                title = listing.find_element(By.XPATH, ".//p[@data-qa-id='aditem_title']").text
                price = listing.find_element(By.XPATH, ".//span[contains(@class, 'price')]").text
                results.append({"title": title, "price": price})
            except Exception as e:
                print(f"Erreur lors de l'extraction d'une annonce : {e}")

        # Sauvegarder les résultats
        with open(OUTPUT_FILE, "w") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"Données enregistrées dans {OUTPUT_FILE}. Nombre d'annonces : {len(results)}")

    except Exception as e:
        print(f"Erreur lors du scraping : {e}")
    finally:
        driver.quit()
        print("Navigateur fermé.")

if __name__ == "__main__":
    scrape_leboncoin()