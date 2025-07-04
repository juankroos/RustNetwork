from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import json
import time
import os
from datetime import datetime

# Configuration
SITE_URL = "https://www.leboncoin.fr/recherche?text=voiture&kst=k&pi=7d4f52cc-5ec6-467f-96b4-c9d24326ac97"
OUTPUT_FILE = "user_actions.json"
DRIVER_PATH = r"E:\RustNetwork\project\src\scrap_py\pro\msedgedriver.exe"  # Chemin vers msedgedriver.exe
EDGE_PROFILE_PATH = r"C:\Users\juankroos\AppData\Local\Microsoft\Edge\User Data"  # Profil Edge
RECORDING_DURATION = 120  # Durée d'enregistrement en secondes (2 minutes)

# Initialiser le navigateur (Microsoft Edge)
options = Options()
options.add_argument("--start-maximized")  # Ouvre le navigateur en plein écran
options.add_argument(f"user-data-dir={EDGE_PROFILE_PATH}")  # Utiliser le profil Edge existant
options.add_argument("--disable-blink-features=AutomationControlled")  # Masquer l'automatisation
options.add_argument("--disable-notifications")  # Désactiver les notifications
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.2592.87")  # User Agent réaliste
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Supprimer l'indicateur d'automatisation

service = Service(DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)

# Masquer navigator.webdriver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Liste pour stocker les actions
actions_log = []

def inject_event_listener():
    """Injecte un script JavaScript pour capturer les interactions."""
    script = """
        window.actionLog = [];
        document.addEventListener('click', function(e) {
            window.actionLog.push({
                type: 'click',
                element: {
                    tag: e.target.tagName,
                    id: e.target.id,
                    class: e.target.className,
                    xpath: getXPath(e.target)
                },
                x: e.clientX,
                y: e.clientY,
                timestamp: Date.now()
            });
        });
        document.addEventListener('keydown', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                window.actionLog.push({
                    type: 'input',
                    element: {
                        tag: e.target.tagName,
                        id: e.target.id,
                        class: e.target.className,
                        xpath: getXPath(e.target)
                    },
                    value: e.target.value,
                    key: e.key,
                    timestamp: Date.now()
                });
            }
        });
        document.addEventListener('scroll', function() {
            window.actionLog.push({
                type: 'scroll',
                scrollX: window.scrollX,
                scrollY: window.scrollY,
                timestamp: Date.now()
            });
        });
        function getXPath(element) {
            if (element.id !== '') return '//*[@id="' + element.id + '"]';
            if (element === document.body) return element.tagName;
            var ix = 0;
            var siblings = element.parentNode.childNodes;
            for (var i = 0; i < siblings.length; i++) {
                var sibling = siblings[i];
                if (sibling === element)
                    return getXPath(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
            }
        }
    """
    driver.execute_script(script)

def save_actions():
    """Récupère les actions enregistrées et les sauvegarde dans un fichier JSON."""
    actions = driver.execute_script("return window.actionLog || [];")
    if actions:
        actions_log.extend(actions)
    # Créer le fichier même s'il est vide
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(actions_log, f, indent=4)
    print(f"Actions enregistrées dans {OUTPUT_FILE}")

try:
    # Accéder à la page d'accueil
    driver.get(SITE_URL)
    print(f"Navigué vers {SITE_URL}. Vous avez {RECORDING_DURATION} secondes pour interagir avec le site.")

    # Injecter l'écouteur d'événements
    inject_event_listener()

    # Attendre 2 minutes
    time.sleep(RECORDING_DURATION)
    print("Les 2 minutes sont écoulées. Enregistrement terminé.")

except Exception as e:
    print(f"Erreur rencontrée : {e}")
finally:
    # Sauvegarder les actions et fermer le navigateur
    save_actions()
    driver.quit()
    print("Navigateur fermé. Consultez le fichier JSON pour les actions enregistrées.")
