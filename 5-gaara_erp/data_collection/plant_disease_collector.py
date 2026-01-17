# /home/ubuntu/gaara_erp_v12/data_collection/plant_disease_collector.py

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class PlantDiseaseCollector:
    def __init__(self, base_dir="/home/ubuntu/gaara_erp_v12/ai_training_data/plant_diseases"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def scrape_images(self, query, num_images=50):
        search_url = f"https://www.bing.com/images/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        image_urls = []
        for img in soup.find_all("img", {"class": "mimg"}, limit=num_images):
            img_url = img.get("src") or img.get("data-src")
            if img_url:
                image_urls.append(img_url)

        self.download_images(query, image_urls)

    def download_images(self, query, urls):
        query_dir = os.path.join(self.base_dir, query.replace(" ", "_"))
        os.makedirs(query_dir, exist_ok=True)
        
        for i, url in enumerate(urls):
            try:
                response = requests.get(url, stream=True, timeout=5)
                if response.status_code == 200:
                    file_path = os.path.join(query_dir, f'{query.replace(" ", "_")}_{i+1}.jpg')
                    with open(file_path, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    print(f"Downloaded {file_path}")
                time.sleep(0.1) # Be respectful
            except Exception as e:
                print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    collector = PlantDiseaseCollector()
    diseases = [
        "tomato late blight",
        "potato early blight",
        "corn common rust",
        "apple scab",
        "grape black rot"
    ]
    for disease in diseases:
        collector.scrape_images(disease, num_images=100)

