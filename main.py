from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import csv
import time

options = Options()
options.headless = True  
options.add_argument("--window-size=1920,1080")  
options.add_argument("--ignore-certificate-errors")  
options.add_argument("start-maximized")  
options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

service = Service("C:/Users/mahij/Downloads/chromedriver-win64/chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.glassdoor.com/Job/entry-level-software-engineer-jobs-in-united-states-jobs-SRCH_KO0,51.htm?fromAge=1")

final_url = driver.current_url
print(f"Redirected to: {final_url}")

all_jobs = []

try:
    while True:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'JobsList_jobListItem__wjTHv'))
        )
        
        time.sleep(5)  
        
        page_source = driver.page_source
        sel = Selector(text=page_source)

        for item in sel.css("li.JobsList_jobListItem__wjTHv"):
            all_jobs.append({
                'title': item.css('a::text').get(),
                'company': item.css('div.jobEmpolyerName::text').get(),
                'location': item.css('div.loc::text').get(),
                'url': item.css('a::attr(href)').get(),
            })

        print(f"Scraped {len(all_jobs)} job listings so far.")

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[data-test="pagination-next"]')
            if next_button.is_enabled():
                next_button.click()
                time.sleep(3)  
            else:
                print("No more pages to scrape.")
                break  
        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            break

    csv_file_path = 'glassdoor_jobs_paginated.csv'
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'company', 'location', 'url'])
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"Data has been written to {csv_file_path}")

finally:
    driver.quit()
