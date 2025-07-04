from bs4 import BeautifulSoup
import json
import os

# Chemin du fichier HTML généré
INPUT_HTML = "page_content.html"
OUTPUT_JSON = "scraped_ads.json"

# Vérifier si le fichier HTML existe
if not os.path.exists(INPUT_HTML):
    print(f"Le fichier {INPUT_HTML} n'existe pas. Vérifiez qu'il a été créé.")
    exit(1)

# Lire et parser le fichier HTML
with open(INPUT_HTML, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Trouver toutes les annonces (exclure les publicités)
ads = []
for li in soup.find_all("li", class_="styles_adCard__JzKik"):
    ad_data = {}
    
    # Extraire l'article principal
    article = li.find("article", {"data-test-id": "ad"})
    if not article:
        continue
    
    # Titre
    title_elem = article.find("p", {"data-test-id": "adcard-title"})
    ad_data["title"] = title_elem.text.strip() if title_elem else "Non spécifié"
    
    # Prix
    price_elem = article.find("p", {"data-test-id": "price"})
    ad_data["price"] = price_elem.text.strip() if price_elem else "Non spécifié"
    
    # Catégorie
    category_elem = article.find("p", {"aria-label": lambda x: x and "Catégorie" in x})
    ad_data["category"] = category_elem.text.strip() if category_elem else "Non spécifié"
    
    # Localisation
    location_elem = article.find("p", {"aria-label": lambda x: x and "Située à" in x})
    ad_data["location"] = location_elem.text.strip() if location_elem else "Non spécifié"
    
    # Date
    date_elem = article.find("p", {"aria-label": lambda x: x and "Date de dépôt" in x})
    ad_data["date"] = date_elem.text.strip() if date_elem else "Non spécifié"
    
    # URL
    url_elem = article.find("a", title=True)
    ad_data["url"] = f"https://www.leboncoin.fr{url_elem['href']}" if url_elem and url_elem.get("href") else "Non spécifié"
    
    # Image
    img_elem = article.find("img")
    ad_data["image_url"] = img_elem["src"] if img_elem and img_elem.get("src") else "Non spécifié"
    
    # Tags
    tags_elem = article.find_all("span", {"data-spark-component": "tag"})
    ad_data["tags"] = [tag.text.strip() for tag in tags_elem] if tags_elem else []
    
    ads.append(ad_data)

# Sauvegarder les données dans un fichier JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(ads, f, indent=4, ensure_ascii=False)
print(f"Données extraites et sauvegardées dans {OUTPUT_JSON}. Nombre d'annonces : {len(ads)}")