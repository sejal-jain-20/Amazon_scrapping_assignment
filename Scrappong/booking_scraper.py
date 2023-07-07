import requests
from bs4 import BeautifulSoup
import csv

# URL of the Amazon product listing page
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Number of pages to scrape (change this value as needed)
num_pages = 20

# List to store scraped data
product_detail = []

# Scrape the product details from each page
for page in range(1, num_pages + 1):
    # Create the URL for the current page
    page_url = url + "&page=" + str(page)
    
    # Send a GET request to the page URL
    response = requests.get(page_url)
    
    # Create a BeautifulSoup object with the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the product items on the page
    product_items = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    # Extract the required information from each product item
    for item in product_items:
        # Extract product URL
        product_url = item.find('a', {'class': 'a-link-normal s-no-outline'})['href']
        
        # Send a GET request to the product URL
        product_response = requests.get("https://www.amazon.in" + product_url)
        
        # Create a BeautifulSoup object with the product page content
        product_soup = BeautifulSoup(product_response.content, 'html.parser')
        
        # Extract ASIN
        asin_element = product_soup.find('th', string='ASIN')
        asin = asin_element.find_next('td').text.strip() if asin_element else None
        
        # Extract product description
        product_description = product_soup.find('div', {'id': 'productDescription'}).text.strip() if product_soup.find('div', {'id': 'productDescription'}) else None
        
        # Extract manufacturer
        manufacturer = product_soup.find('a', {'id': 'bylineInfo'}).text.strip() if product_soup.find('a', {'id': 'bylineInfo'}) else None
        
        # Extract product name
        product_name = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        
        # Extract product price
        product_price_element = item.find('span', {'class': 'a-price-whole'})
        product_price = product_price_element.text if product_price_element else None
        
        # Extract rating
        rating = item.find('span', {'class': 'a-icon-alt'}).text.split()[0]
        
        # Extract number of reviews
        num_reviews = item.find('span', {'class': 'a-size-base'}).text
        
        # Create a dictionary to store the product details
        product_info = {
            'URL': product_url,
            'Name': product_name,
            'Price': product_price,
            'Rating': rating,
            'Reviews': num_reviews,
            'Description': product_description,
            'ASIN': asin,
            'Manufacturer': manufacturer
        }
        
        # Append the product info to the list
        product_detail.append(product_info)
        
        # Check if the desired number of URLs is reached
        if len(product_detail) >= 200:
            break
    
    # Check if the desired number of URLs is reached
    if len(product_detail) >= 200:
        break

# Export data to CSV file
csv_file = 'product_detail.csv'
headers = ['URL', 'Name', 'Price', 'Rating', 'Reviews', 'Description', 'ASIN', 'Manufacturer']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(product_detail)

print(f"Data exported to {csv_file} successfully.")
