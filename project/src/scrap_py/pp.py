from flask import Flask, request, jsonify
import json
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from fake_useragent import UserAgent
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration de Flask
app = Flask(__name__)

# Configuration des logs
import logging
logging.basicConfig(level=logging.INFO, filename="scraper.log", format="%(asctime)s - %(levelname)s - %(message)s")

# Liste de délais pour simuler un comportement humain
HUMAN_DELAYS = [3, 4, 5, 6, 7]  # Augmentés pour plus de furtivité

# Nombre maximum de tentatives pour les retries
MAX_RETRIES = 3

# Nombre maximum de threads pour le scraping parallèle
MAX_WORKERS = 1  # Un seul thread pour éviter les blocages

# URL par défaut pour tester
DEFAULT_URL = "https://www.leboncoin.fr/recherche?category=10&text=iphone"

def get_random_user_agent():
    """Retourne un User-Agent aléatoire."""
    ua = UserAgent()
    return ua.random

def setup_driver():
    """Configure le navigateur Edge avec un User-Agent aléatoire."""
    options = Options()
    options.add_argument(f"user-agent={get_random_user_agent()}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
        """
    })
    return driver

def simulate_human_mouse(driver, x, y):
    """Simule un mouvement de souris humain."""
    try:
        actions = ActionChains(driver)
        current_x, current_y = random.randint(0, 100), random.randint(0, 100)
        steps = 10
        for _ in range(steps):
            actions.move_by_offset(
                (x - current_x) / steps + random.uniform(-5, 5),
                (y - current_y) / steps + random.uniform(-5, 5)
            ).pause(random.uniform(0.1, 0.3)).perform()
            current_x += (x - current_x) / steps
            current_y += (y - current_y) / steps
    except Exception as e:
        logging.warning(f"Erreur lors de la simulation de souris: {e}")

def simulate_human_behavior(driver):
    """Ajoute des comportements humains (défilements, pauses)."""
    try:
        scroll_distance = random.randint(100, 500)
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.choice(HUMAN_DELAYS))
        simulate_human_mouse(driver, random.randint(100, 800), random.randint(100, 600))
    except Exception as e:
        logging.warning(f"Erreur lors de la simulation de comportement: {e}")

def check_for_honeypot(driver):
    """Vérifie la présence de honeypots."""
    honeypot_indicators = [
        "display: none",
        "visibility: hidden",
        "opacity: 0",
        "position: absolute; left: -9999px"
    ]
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, "a, input, button")
        for element in elements:
            style = driver.execute_script("return window.getComputedStyle(arguments[0]).cssText;", element)
            if any(indicator in style for indicator in honeypot_indicators):
                logging.warning(f"Piège détecté (honeypot): {style}")
                return True
    except Exception as e:
        logging.warning(f"Erreur lors de la vérification des honeypots: {e}")
    return False

def check_for_redirection(driver, expected_url):
    """Vérifie si une redirection suspecte a eu lieu."""
    try:
        current_url = driver.current_url
        parsed_expected = urlparse(expected_url)
        parsed_current = urlparse(current_url)
        if parsed_expected.netloc != parsed_current.netloc:
            logging.warning(f"Redirection suspecte détectée: {current_url}")
            return True
    except Exception as e:
        logging.warning(f"Erreur lors de la vérification de redirection: {e}")
    return False

def check_for_anti_scraping_scripts(driver):
    """Vérifie la présence de scripts anti-scraping."""
    try:
        scripts = driver.find_elements(By.TAG_NAME, "script")
        for script in scripts:
            src = script.get_attribute("src") or ""
            content = driver.execute_script("return arguments[0].innerHTML;", script) or ""
            if any(keyword in (src + content).lower() for keyword in ["bot", "crawler", "scrap", "fingerprint"]):
                logging.warning(f"Script anti-scraping potentiel détecté: {src}")
                return True
    except Exception as e:
        logging.warning(f"Erreur lors de la vérification des scripts anti-scraping: {e}")
    return False

def check_for_captcha(driver):
    """Vérifie la présence d’un CAPTCHA et attend la résolution manuelle."""
    try:
        if "g-recaptcha" in driver.page_source:
            print("CAPTCHA détecté. Résolvez-le manuellement dans le navigateur, puis appuyez sur Entrée ici pour continuer...")
            input("Appuyez sur Entrée après avoir résolu le CAPTCHA...")
            if "g-recaptcha" not in driver.page_source:
                logging.info("CAPTCHA résolu manuellement avec succès")
                return True
            logging.error("Échec de la résolution manuelle du CAPTCHA")
            print("Erreur: Échec de la résolution manuelle du CAPTCHA")
            return False
    except Exception as e:
        logging.error(f"Erreur lors de la vérification du CAPTCHA: {e}")
        print(f"Erreur lors de la vérification du CAPTCHA: {e}")
    return True

def scrape_leboncoin_page(driver, attempt=1):
    """Extrait les titres, prix et URLs des annonces sur une page de résultats Leboncoin."""
    try:
        print(f"Tentative {attempt} de scraping de la page...")
        ad_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'styles_AdItem__') or contains(@class, 'aditem')]")
        print(f"Nombre d'annonces trouvées: {len(ad_elements)}")
        results = []
        for ad in ad_elements[:5]:  # Limite à 5 annonces
            try:
                # Mise à jour des XPaths pour être plus génériques
                title_element = ad.find_elements(By.XPATH, ".//span[contains(@class, 'title') or contains(@class, 'Title')]")
                price_element = ad.find_elements(By.XPATH, ".//span[contains(@class, 'price') or contains(@class, 'Price')]")
                ad_url_element = ad.find_elements(By.XPATH, ".//a")
                
                title = title_element[0].text if title_element else "Titre non trouvé"
                price = price_element[0].text if price_element else "Prix non trouvé"
                ad_url = ad_url_element[0].get_attribute("href") if ad_url_element else "URL non trouvée"
                
                results.append({"title": title, "price": price, "ad_url": ad_url})
            except Exception as e:
                logging.warning(f"Erreur lors de l'extraction d'une annonce: {e}")
                print(f"Erreur lors de l'extraction d'une annonce: {e}")
        return results
    except Exception as e:
        logging.error(f"Erreur lors du scraping de la page (tentative {attempt}): {e}")
        print(f"Erreur lors du scraping de la page (tentative {attempt}): {e}")
        if attempt < MAX_RETRIES:
            time.sleep(random.uniform(2, 5))
            return scrape_leboncoin_page(driver, attempt + 1)
        return []

def scrape_single_url(url, actions_log, search_query, attempt=1):
    """Scrape une seule URL de Leboncoin et affiche les résultats dans la console."""
    driver = setup_driver()
    try:
        print(f"Accès à l'URL: {url}")
        driver.get(url)
        time.sleep(random.choice(HUMAN_DELAYS))  # Attente initiale pour charger la page
        
        if not check_for_captcha(driver):
            print(f"Erreur pour {url}: Échec résolution CAPTCHA (manuel)")
            return {"error": "Échec résolution CAPTCHA (manuel)"}
        
        if check_for_redirection(driver, url) or check_for_anti_scraping_scripts(driver):
            logging.error(f"Arrêt: piège anti-scraping ou redirection détecté (tentative {attempt})")
            print(f"Erreur pour {url}: Piège anti-scraping ou redirection détecté (tentative {attempt})")
            if attempt < MAX_RETRIES:
                time.sleep(random.uniform(5, 10))
                driver.quit()
                return scrape_single_url(url, actions_log, search_query, attempt + 1)
            return {"error": "Piège anti-scraping ou redirection détecté"}
        
        if search_query:
            print(f"Simulation de la recherche pour: {search_query}")
            try:
                search_input = driver.find_element(By.XPATH, "//input[@name='q' or @placeholder[contains(., 'recherche')]]")
                search_input.clear()
                search_input.send_keys(search_query)
                time.sleep(random.choice(HUMAN_DELAYS))
                
                submit_button = driver.find_element(By.XPATH, "//button[@type='submit' or contains(@class, 'search') or contains(., 'Rechercher')]")
                submit_button.click()
                time.sleep(random.choice(HUMAN_DELAYS))
            except Exception as e:
                logging.warning(f"Erreur lors de la simulation de recherche: {e}")
                print(f"Erreur lors de la simulation de recherche: {e}")
        
        simulate_human_behavior(driver)
        results = scrape_leboncoin_page(driver)
        
        if not results:
            print(f"Aucun résultat trouvé pour {url}")
        else:
            print(f"\nRésultats extraits pour {url}:")
            for result in results:
                print(f"Titre: {result['title']}")
                print(f"Prix: {result['price']}")
                print(f"URL de l'annonce: {result['ad_url']}")
                print(f"Timestamp: {datetime.now().isoformat()}")
                print("-" * 50)
        
        return {"data": results}
    except Exception as e:
        logging.error(f"Erreur générale lors du scraping de {url} (tentative {attempt}): {e}")
        print(f"Erreur pour {url}: {str(e)}")
        if attempt < MAX_RETRIES:
            time.sleep(random.uniform(5, 10))
            driver.quit()
            return scrape_single_url(url, actions_log, search_query, attempt + 1)
        return {"error": str(e)}
    finally:
        driver.quit()

@app.route("/scrape", methods=["POST"])
def scrape():
    """API endpoint pour lancer le scraping sur Leboncoin."""
    data = request.get_json()
    urls = data.get("urls", [DEFAULT_URL])  # Utilise l'URL par défaut si aucune n'est fournie
    search_query = data.get("search_query", "")
    actions_log = data.get("actions_log", [])
    
    if not urls:
        return jsonify({"error": "Liste d'URLs requise"}), 400
    
    print(f"Lancement du scraping pour les URLs: {urls}")
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(scrape_single_url, url, actions_log, search_query): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append({"url": url, "result": result})
            except Exception as e:
                results.append({"url": url, "error": str(e)})
                print(f"Erreur pour {url}: {str(e)}")
    
    return jsonify({"results": results})

@app.route("/results", methods=["GET"])
def view_results():
    """Affiche un message indiquant que les résultats sont dans la console."""
    return jsonify({"message": "Les résultats sont affichés dans la console."})

# Interface en ligne de commande pour tester
def test_scraper():
    """Teste le scraper avec l'URL par défaut."""
    print(f"Test du scraper avec l'URL: {DEFAULT_URL}")
    result = scrape_single_url(DEFAULT_URL, [], "iphone")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    # Décommentez pour tester directement sans Flask
    test_scraper()
    
    # Lancement de l'application Flask
    # app.run(debug=True, host="0.0.0.0", port=5000)