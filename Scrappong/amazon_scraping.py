import requests
from bs4 import BeautifulSoup
import csv

# URL of the Amazon product listing page
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Number of pages to scrape (change this value as needed)
num_pages = 20

# List to store scraped data
product_data = []

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
        
        # Extract product name
        product_name = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        
        # Extract product price
        product_price = item.find('span', {'class': 'a-price-whole'}).text
        
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
            'Reviews': num_reviews
        }
        
        # Append the product info to the list
        product_data.append(product_info)

# Export data to CSV file
csv_file = 'product_data.csv'
headers = ['URL', 'Name', 'Price', 'Rating', 'Reviews']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(product_data)

print(f"Data exported to {csv_file} successfully.")
