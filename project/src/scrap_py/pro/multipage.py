from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os
import pickle
from fake_useragent import UserAgent

# Configuration
BASE_URL = "https://www.leboncoin.fr/recherche?text=voiture&kst=k&pi=7d4f52cc-5ec6-467f-96b4-c9d24326ac97"
OUTPUT_DIR = "pages"
DRIVER_PATH = r"E:\RustNetwork\project\src\scrap_py\pro\msedgedriver.exe"
EDGE_PROFILE_PATH = r"C:\Users\juankroos\AppData\Local\Microsoft\Edge\User Data"
COOKIES_PATH = r"E:\RustNetwork\project\src\scrap_py\pro\cookies.pkl"
PROXY_LIST = [
    "http://user:pass@ip1:port",  # Remplacez par vos proxys
    "http://user:pass@ip2:port",
]

# Créer le répertoire de sortie
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Initialiser User Agent
ua = UserAgent()

def init_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument(f"user-data-dir={EDGE_PROFILE_PATH}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument(f"user-agent={ua.random}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # Décommentez si vous avez des proxys
    # options.add_argument(f"--proxy-server={random.choice(PROXY_LIST)}")

    service = Service(DRIVER_PATH)
    try:
        return webdriver.Edge(service=service, options=options)
    except Exception as e:
        print(f"Erreur lors de l'initialisation du driver : {e}")
        exit(1)

# Masquer navigator.webdriver
def configure_driver(driver):
    try:
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = { runtime: {} };
            """
        })
    except Exception as e:
        print(f"Erreur lors de la configuration anti-détection : {e}")



def human_scroll(driver, pixels=500):
    try:
        driver.execute_script(f"window.scrollBy(0, {pixels});")
        time.sleep(random.uniform(1.0, 2.0))
    except Exception as e:
        print(f"Erreur lors du défilement : {e}")

def save_cookies(driver, path=COOKIES_PATH):
    try:
        with open(path, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
        print(f"Cookies sauvegardés dans {path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des cookies : {e}")

def load_cookies(driver, path=COOKIES_PATH):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    try:
                        driver.add_cookie(cookie)
                    except Exception as e:
                        print(f"Erreur lors de l'ajout du cookie {cookie['name']}: {e}")
            print(f"Cookies chargés depuis {path}")
        else:
            print("Aucun fichier de cookies trouvé.")
    except Exception as e:
        print(f"Erreur lors du chargement des cookies : {e}")

def check_for_captcha(driver):
    try:
        captcha = driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')] | //div[contains(text(), 'vérification') or contains(text(), 'captcha')]")
        print("CAPTCHA ou page de vérification détecté. Résolution manuelle requise ou utilisez un service comme 2Captcha.")
        return True
    except:
        return False

def scrape_all_pages():
    driver = init_driver()
    configure_driver(driver)
    current_page = 1

    while True:
        try:
            print(f"Étape 1 : Chargement de la page {current_page}...")
            if current_page == 1:
                driver.get(BASE_URL)
            else:
                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-spark-component='pagination-next-trigger']"))
                )
                next_url = next_button.get_attribute("href")
                if not next_url or next_url == driver.current_url:
                    print(f"Fin des pages atteintes à la page {current_page}.")
                    break
                driver.get(next_url)
            load_cookies(driver)
            driver.get(driver.current_url)  # Recharger pour appliquer les cookies
            time.sleep(random.uniform(5.0, 10.0))

            # Vérifier le CAPTCHA
            page_title = driver.title
            print(f"Étape 2 : Titre de la page : {page_title}")
            if "reCAPTCHA" in page_title.lower() or "vérification" in page_title.lower():
                print("Redirection vers une page de vérification détectée.")
                if check_for_captcha(driver):
                    driver.save_screenshot(f"captcha_screenshot_page{current_page}.png")
                    print(f"Screenshot de la page de CAPTCHA sauvegardé : captcha_screenshot_page{current_page}.png")
                    input(f"Résolvez le CAPTCHA manuellement pour la page {current_page}, puis appuyez sur Entrée pour continuer...")
                    save_cookies(driver)

            # Défilement pour charger les annonces
            print(f"Étape 3 : Défilement de la page {current_page}...")
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                human_scroll(driver, pixels=random.randint(300, 600))
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Sauvegarder le HTML
            print(f"Étape 4 : Sauvegarde du HTML pour la page {current_page}...")
            html_content = driver.page_source
            output_file = os.path.join(OUTPUT_DIR, f"page_{current_page}.html")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"HTML sauvegardé dans {output_file}")

            current_page += 1

        except Exception as e:
            print(f"Erreur lors du scraping de la page {current_page} : {e}")
            driver.save_screenshot(f"error_screenshot_page{current_page}.png")
            print(f"Screenshot sauvegardé : error_screenshot_page{current_page}.png")
            # Tentative de redémarrage
            try:
                driver.quit()
                driver = init_driver()
                configure_driver(driver)
                load_cookies(driver)
                print("Driver redémarré. Reprise possible manuelle.")
                input("Appuyez sur Entrée pour reprendre ou Ctrl+C pour arrêter.")
            except Exception as e2:
                print(f"Échec du redémarrage du driver : {e2}")
                break
            finally:
                #driver.quit()
                print(f"Étape 6 : Navigation terminée. Total pages scrapées : {current_page - 1}")

if __name__ == "__main__":
    scrape_all_pages()