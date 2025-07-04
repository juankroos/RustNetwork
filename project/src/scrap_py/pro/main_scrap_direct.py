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
SITE_URL = "https://www.leboncoin.fr/recherche?text=voiture&kst=k&pi=7d4f52cc-5ec6-467f-96b4-c9d24326ac97"
#SITE_URL = 'https://www.leboncoin.fr/recherche?text=Toute+la+France&kst=k&pi=94c75cb2-a5b4-4a4e-93b5-408843386649'
OUTPUT_HTML = "page_content.html"
DRIVER_PATH = r"E:\RustNetwork\project\src\scrap_py\pro\msedgedriver.exe"
EDGE_PROFILE_PATH = r"C:\Users\juankroos\AppData\Local\Microsoft\Edge\User Data"
COOKIES_PATH = r"E:\RustNetwork\project\src\scrap_py\pro\cookies.pkl"
PROXY_LIST = [
    "http://user:pass@ip1:port",  # Remplacez par vos proxys
    "http://user:pass@ip2:port",
]

# Vérifier et créer le répertoire de sortie
output_dir = os.path.dirname(OUTPUT_HTML) or "."
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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
# Décommentez la ligne suivante si vous avez des proxys valides
# options.add_argument(f"--proxy-server={random.choice(PROXY_LIST)}")

service = Service(DRIVER_PATH)
try:
    driver = webdriver.Edge(service=service, options=options)
except Exception as e:
    print(f"Erreur lors de l'initialisation du driver : {e}")
    exit(1)

# Masquer navigator.webdriver et autres indicateurs
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
    """Simule un défilement humain."""
    try:
        driver.execute_script(f"window.scrollBy(0, {pixels});")
        time.sleep(random.uniform(1.0, 2.0))
    except Exception as e:
        print(f"Erreur lors du défilement : {e}")

def save_cookies(driver, path=COOKIES_PATH):
    """Sauvegarde les cookies."""
    try:
        with open(path, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
        print(f"Cookies sauvegardés dans {path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des cookies : {e}")

def load_cookies(driver, path=COOKIES_PATH):
    """Charge les cookies."""
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
    """Vérifie la présence d'un CAPTCHA."""
    try:
        captcha = driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')] | //div[contains(text(), 'vérification') or contains(text(), 'captcha')]")
        print("CAPTCHA ou page de vérification détecté. Résolution manuelle requise ou utilisez un service comme 2Captcha.")
        return True
    except:
        return False

def scrape_leboncoin():
    """Récupère le HTML brut de la page après chargement complet."""
    try:
        # Charger les cookies
        print("Étape 1 : Chargement de la page initiale...")
        driver.get(SITE_URL)
        load_cookies(driver)
        driver.get(SITE_URL)  # Recharger pour appliquer les cookies
        time.sleep(random.uniform(5.0, 10.0))  # Attente pour le chargement initial

        # Vérifier le titre de la page pour détecter une redirection
        page_title = driver.title
        print(f"Étape 2 : Titre de la page : {page_title}")
        if "reCAPTCHA" in page_title.lower() or "vérification" in page_title.lower():
            print("Redirection vers une page de vérification détectée.")
            #if check_for_captcha(driver):
                #driver.save_screenshot("captcha_screenshot.png")
                #print("Screenshot de la page de CAPTCHA sauvegardé : captcha_screenshot.png")
                #input("Résolvez le CAPTCHA manuellement, puis appuyez sur Entrée pour continuer...")
                #save_cookies(driver)

        # Faire défiler la page pour charger toutes les annonces
        print("Étape 3 : Défilement de la page...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            human_scroll(driver, pixels=random.randint(300, 600))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Récupérer et sauvegarder le HTML brut
        print("Étape 4 : Récupération du HTML brut...")
        html_content = driver.page_source
        with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Étape 5 : HTML brut sauvegardé dans {OUTPUT_HTML}")

    except Exception as e:
        print(f"Erreur lors du scraping : {e}")
        driver.save_screenshot("error_screenshot.png")
        print("Screenshot de la page sauvegardé : error_screenshot.png")
    finally:
        driver.quit()
        print("Étape 6 : Navigateur fermé.")

if __name__ == "__main__":
    scrape_leboncoin()