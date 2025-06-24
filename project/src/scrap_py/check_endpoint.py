import requests
import sys

# Fonction pour vérifier si un endpoint existe
def check_endpoint(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[+] Endpoint trouvé : {url} (Code: {response.status_code})")
            print(f"    Headers du serveur : {response.headers.get('Server', 'Non spécifié')}")
            return True
        else:
            print(f"[-] Endpoint non accessible : {url} (Code: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[!] Erreur lors de l'accès à {url} : {e}")
        return False

# Fonction principale
def main():
    if len(sys.argv) != 2:
        print("Usage : python script.py <IP_ou_URL>")
        sys.exit(1)

    target = sys.argv[1]
    if not target.startswith("http"):
        target = f"http://{target}"

    print(f"[*] Cible : {target}")
    print("[*] Début de l'énumération...")

    # Liste d'endpoints courants à vérifier
    endpoints = [
        "/", "/index.html", "/admin", "/login", "/phpinfo.php", 
        "/.htaccess", "/config", "/backup", "/api","/test", "/wp-admin"
    ]

    # Vérification des endpoints
    for endpoint in endpoints:
        check_endpoint(f"{target}{endpoint}")

    # Vérification des méthodes HTTP supportées
    try:
        response = requests.options(target)
        print(f"[*] Méthodes HTTP supportées : {response.headers.get('Allow', 'Non spécifié')}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Erreur lors de la vérification des méthodes HTTP : {e}")

if __name__ == "__main__":
    main()