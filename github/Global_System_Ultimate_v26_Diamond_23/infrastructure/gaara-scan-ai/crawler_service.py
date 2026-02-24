import os
import time
import requests
import logging
from datetime import datetime
import psycopg2
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Connection
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="ml_db",
        user="user",
        password="password"
    )
    return conn

# OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def search_inaturalist(query):
    logger.info(f"Searching iNaturalist for: {query}")
    url = f"https://api.inaturalist.org/v1/observations?q={query}&per_page=10"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def verify_image_with_vision(image_url, label):
    logger.info(f"Verifying image {image_url} for label {label}...")
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Is this an image of {label}? Answer with YES or NO."},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            max_tokens=10,
        )
        answer = response.choices[0].message.content.strip().upper()
        return "YES" in answer
    except Exception as e:
        logger.error(f"Vision API error: {e}")
        return False

def run_crawler():
    search_terms = ["tomato early blight", "potato late blight", "corn rust"]
    
    for term in search_terms:
        results = search_inaturalist(term)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        images_found = 0
        for result in results:
            photos = result.get('photos', [])
            if not photos:
                continue
                
            image_url = photos[0].get('url').replace("square", "medium")
            
            # Check for duplicates
            cur.execute("SELECT id FROM image_catalog WHERE image_url = %s", (image_url,))
            if cur.fetchone():
                logger.info(f"Duplicate found: {image_url}")
                continue
            
            # Verify with Vision
            is_verified = verify_image_with_vision(image_url, term)
            
            # Save to DB
            cur.execute(
                "INSERT INTO image_catalog (image_url, source, label, is_verified) VALUES (%s, %s, %s, %s)",
                (image_url, "inaturalist", term, is_verified)
            )
            images_found += 1
            
        # Update tracking
        cur.execute(
            "INSERT INTO crawler_tracking (search_term, images_found) VALUES (%s, %s)",
            (term, images_found)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"Crawler run complete for {term}. Found {images_found} new images.")

if __name__ == "__main__":
    while True:
        run_crawler()
        time.sleep(3600) # Run every hour
