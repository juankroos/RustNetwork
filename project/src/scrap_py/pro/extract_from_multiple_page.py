from bs4 import BeautifulSoup
import json
import os

# Chemins
OUTPUT_DIR = "pages"
OUTPUT_JSON = "scraped_ads_final.json"

# Vérifier si le répertoire existe
if not os.path.exists(OUTPUT_DIR):
    print(f"Le répertoire {OUTPUT_DIR} n'existe pas. Vérifiez qu'il a été créé.")
    exit(1)

# Initialiser la liste des annonces
ads = []

# Parcourir tous les fichiers HTML dans le répertoire
for filename in os.listdir(OUTPUT_DIR):
    if filename.endswith(".html"):
        file_path = os.path.join(OUTPUT_DIR, filename)
        print(f"Traitement du fichier : {file_path}")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            # Trouver toutes les annonces (exclure les publicités)
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
                
                # Ajouter des métadonnées (optionnel)
                ad_data["page_source"] = filename.replace(".html", "")
                
                ads.append(ad_data)

        except Exception as e:
            print(f"Erreur lors du traitement de {file_path} : {e}")
            continue

# Sauvegarder les données dans un fichier JSON
if ads:
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ads, f, indent=4, ensure_ascii=False)
    print(f"Données extraites et sauvegardées dans {OUTPUT_JSON}. Nombre total d'annonces : {len(ads)}")
else:
    print("Aucune annonce extraite. Vérifiez les fichiers HTML.")