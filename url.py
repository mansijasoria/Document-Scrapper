
#dont use this code 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def extract_sciencedirect_info_selenium(url):
    # Set up the Selenium driver (make sure to specify the path to your ChromeDriver)
    options = Options()
    options.headless = True
    service = Service('C:/Users/Mansi Jasoria/Desktop/IIT/chromedriver_win32')
    driver = webdriver.Chrome(service=service, options=options)

    # Use Selenium to get the page with JavaScript executed
    driver.get(url)
    time.sleep(5)  # Wait for


# Now that the page is loaded, we can use BeautifulSoup to parse it
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the driver
    driver.quit()

    # Extracting title
    title = soup.find('span', class_='title-text')
    title = title.get_text(strip=True) if title else 'Title not found'

    # Extracting journal name
    journal_name = soup.find('a', class_='publication-title-link')
    journal_name = journal_name.get_text(strip=True) if journal_name else 'Journal name not found'

    # Extracting authors
    authors = soup.find_all('a', class_='author')
    author_list = []
    for author in authors:
        name = author.find('span', class_='text given-name').get_text(strip=True) + " " + \
            author.find('span', class_='text surname').get_text(strip=True)
        # The affiliation data may be in a different format or not available without further interaction
        author_list.append(name)

    return {
        'Title': title,
        'Journal Name': journal_name,
        'Authors': author_list
}

url='https://www.sciencedirect.com/science/article/pii/S2090123221001491'
    