from bs4 import BeautifulSoup
import requests
import json
import pandas as pd  # Import pandas

walmart_url = "https://www.walmart.com/ip/LG-34-UltraGear-Quad-HD-3440-x-1440-2K-160Hz-OC-1ms-2xHDMI-DisplayPort-Radeon-FreeSync-2-NVIDIA-G-Sync-Compatible-USB-3-0-Hub-Nano-IPS-Curved-Gaming/507169893?from=/search"
HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

# Function to extract product information
def extract_productInfo(product_url):
    response = requests.get(product_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    script_tag = soup.find("script", id="__NEXT_DATA__")
    data = json.loads(script_tag.string)
    initial_data = data['props']['pageProps']['initialData']['data']
    product_data = initial_data['product']
    review_data = initial_data.get("reviews", {})
    
    product_info = {
        "price": product_data['priceInfo']['currentPrice']['price'],
        "review_count": review_data.get('totalReviewCount', 0),
        "item_id": product_data['usItemId'],
        "avg_rating": review_data.get("averageOverallRating", 0),
        "product_name": product_data['name'],
        "brand": product_data.get("brand", ""),
        "availability": product_data['availabilityStatus'],
        "image_url": product_data['imageInfo']['thumbnailUrl'],
        "short_description": product_data.get("shortDescription", "")
    }
    
    return product_info

# Function to get product links from search results
def get_productLinks(query, page_number=1):
    search_url = f"https://www.walmart.com/search?q={query}&page={page_number}"
    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)
    
    product_links = []
    
    for link in links:
        link_href = link['href']
        if "/ip" in link_href:
            if "https" in link_href:
                full_url = link_href
            else:
                full_url = "https://www.walmart.com" + link_href
            
            product_links.append(full_url)
    
    return product_links

product_info_list = []
seen_urls = set() 

for page_number in range(1, 6):
    links = get_productLinks("computers", page_number)
    
    if not links:
        break
    
    for link in links:
        try:
            if link not in seen_urls: 
                product_info = extract_productInfo(link)
                if product_info:
                    product_info_list.append(product_info)
                    seen_urls.add(link)
            else:
                print(f"Skipping duplicate URL: {link}")
        except Exception as e:
            print(f"Failed to Process URL {link}. Error: {e}")
    
    print(f"Search Page {page_number} scraped.")

# Converting list of dictionaries to DataFrame
df = pd.DataFrame(product_info_list)

# Saving DataFrame to CSV file
OUTPUT_FILE = "product_info.csv"
df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved scraped data to {OUTPUT_FILE}")
