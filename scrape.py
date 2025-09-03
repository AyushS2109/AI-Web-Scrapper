import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from scrapeLinks import (
    extract_links,
    find_correct_link,
)
import time

def scrape_website(website, query):
    # print("Launching Chrome Browser")

    chrome_driver_path = "./chromedriver"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options = options)

    try:
        driver.get(website)
        # print("Page Loaded")
        WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        body_content = soup.body
        # print(type(body_content))
        div_texts, links = extract_links(str(body_content))
        link = find_correct_link(div_texts, links, query)
        url = "https://flipkart.com"+link
        try:
            driver.get(url)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            html = driver.page_source
        except: pass

        return html

    finally:
        driver.quit()
        # print(html)

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    # cleaned_content = body_content
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i+max_length] for i in range(0, len(dom_content),max_length)
    ]