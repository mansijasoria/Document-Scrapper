from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Specify the path to chromedriver executable
service = Service('path')

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service)

# URL of the article
url = "https://www.sciencedirect.com/science/article/pii/S2090123221001491"

# Go to the specified URL
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Extract information
journal_name = driver.find_element(By.CSS_SELECTOR, "publication-title-link").text
doi_element = driver.find_element(By.CLASS_NAME, "doi")
doi = doi_element.text if doi_element else "DOI not found"
publication_date_element = driver.find_element(By.CLASS_NAME, "history-dates")
publication_date = publication_date_element.text if publication_date_element else "Publication date not found"
article_type_element = driver.find_element(By.CLASS_NAME, "article-type")
article_type = article_type_element.text if article_type_element else "Article type not found"

authors_elements = driver.find_elements(By.CSS_SELECTOR, "div.author-group > a.author")
authors = [author.text for author in authors_elements] if authors_elements else ["Author information not available"]

corresponding_authors_elements = driver.find_elements(By.CSS_SELECTOR, "div.author-group a.correspondence-email")
corresponding_authors = [corr_author.get_attribute('title') for corr_author in corresponding_authors_elements] if corresponding_authors_elements else ["Corresponding author information not available"]

# Close the browser
driver.quit()

# Display the extracted information
print("Journal Name:", journal_name)
print("DOI:", doi)
print("Publication Date:", publication_date)
print("Article Type:", article_type)
print("Authors:", authors)
print("Corresponding Authors:", corresponding_authors)

