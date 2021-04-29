import requests
from bs4 import BeautifulSoup
import threading
import time
import concurrent.futures

print('type your unfamiliar skill')
unfamiliar_skill=input('>')

#decide how many page you wnat to scrape
print('How many pages you want to scrap?')
Page_want = int(input('>'))
print("Filtering out your unfamiliar skill")

def scrapy_1page(urls):
    html_text= requests.get(urls).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    my_file = open('jobpost.txt', 'w')
    for job in jobs:
        posted_date=job.find('span', class_='sim-posted')
        
        
        if 'few' or '1' or '2' or '3' in posted_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ','')
            skills = job.find('span', class_='srp-skills').text.replace(' ','')

            more_info = job.header.h2.a['href']
            
            if unfamiliar_skill not in skills:
                my_file.write(f"Company Name: {company_name.strip()}\n")
                my_file.write(f"Skills: {skills.strip()}\n")
                my_file.write(f"More information: {more_info}\n")

                print()
                print(f"Company Name: {company_name.strip()}")
                print(f"Skills: {skills.strip()}")
                print(f"More information: {more_info}")
                print()
                
    my_file.close()           
    time.sleep(5)

base_url="https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=intern&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=intern&pDate=I&sequence="
urls=[f'{base_url}{page}&startPage=1' for page in range(1,Page_want + 1)]#page from 1 to 8            
print(urls)
start_time = time.time()  # time start
 
# create ten thread
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scrapy_1page, urls)
 
end_time = time.time() # time finish
print(f"{end_time - start_time} seconds for {len(urls)} pages")     



