import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import IgnoreRequest
import pandas as pd
import json
import time

class LinkedinProfileItem(scrapy.Item):
    linkedin_url = scrapy.Field()
    name = scrapy.Field()
    bio = scrapy.Field()
    socials = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()

class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': True,
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 1,
        'HANDLE_HTTPSTATUS_LIST': [999, 403, 401, 404],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700
        },
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate, br'
        }
    }

    def __init__(self, linkedin_email='', linkedin_password='', *args, **kwargs):
        super(LinkedinSpider, self).__init__(*args, **kwargs)
        self.linkedin_email = linkedin_email
        self.linkedin_password = linkedin_password

    def start_requests(self):
        
        yield scrapy.Request(
            url='https://www.linkedin.com',
            callback=self.parse_homepage,
            dont_filter=True
        )

    def parse_homepage(self, response):
       
        csrf_token = response.xpath('//input[@name="csrfToken"]/@value').get()
        if not csrf_token:
            csrf_token = response.headers.getlist('Set-Cookie')[0].decode().split('JSESSIONID=')[1].split(';')[0]

       
        login_data = {
            'session_key': self.linkedin_email,
            'session_password': self.linkedin_password,
            'csrfToken': csrf_token,
            'loginCsrfParam': csrf_token,
        }

        yield scrapy.FormRequest(
            url='https://www.linkedin.com/checkpoint/lg/login-submit',
            formdata=login_data,
            callback=self.after_login,
            dont_filter=True
        )

    def after_login(self, response):
       
        if response.status == 200:
            self.logger.info("Successfully logged in. Starting to scrape profiles...")
            
            try:
                df = pd.read_excel("Assignment.xlsx")
                urls = df["LinkedIn URLs"].tolist()
                
                for url in urls:
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse_profile,
                        meta={'linkedin_url': url},
                        dont_filter=True,
                        errback=self.handle_error
                    )
            except Exception as e:
                self.logger.error(f"Error reading Excel file: {str(e)}")
        else:
            self.logger.error(f"Login failed with status code: {response.status}")

    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.value}")
        if failure.check(IgnoreRequest):
            self.logger.warning(f"Request ignored for URL: {failure.request.url}")

    def parse_profile(self, response):
        if response.status in [999, 403, 401]:
            self.logger.warning(f"Received status {response.status} for {response.url}. Retrying after delay...")
            time.sleep(10)
            yield scrapy.Request(
                url=response.url,
                callback=self.parse_profile,
                meta=response.meta,
                dont_filter=True
            )
            return

        item = LinkedinProfileItem()
        item['linkedin_url'] = response.meta['linkedin_url']

        try:
           
            item['name'] = response.css('h1.top-card-layout__title::text').get()
            item['bio'] = response.css('div.top-card-layout__summary::text').get()
            
          
            item['experience'] = {}
            experience_items = response.css('li.experience-item')
            for exp in experience_items:
                company = exp.css('.experience-item__subtitle::text').get()
                role = exp.css('.experience-item__title::text').get()
                if company and role:
                    item['experience'][company.strip()] = role.strip()

           
            item['education'] = {}
            education_items = response.css('li.education__list-item')
            for edu in education_items:
                school = edu.css('.education__school-name::text').get()
                degree = edu.css('.education__item--degree-info::text').get()
                if school and degree:
                    item['education'][school.strip()] = degree.strip()

        except Exception as e:
            self.logger.error(f"Error parsing profile {response.url}: {str(e)}")
            item['name'] = None
            item['bio'] = None
            item['experience'] = {}
            item['education'] = {}

        yield item

class LinkedinPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        if self.items:
            df = pd.DataFrame(self.items)
            df.to_csv('scraped_output.csv', index=False)
        else:
            with open('scraped_output.csv', 'w') as f:
                f.write('No data was scraped')

if __name__ == "__main__":
    linkedin_email = input("Enter your LinkedIn email: ")
    linkedin_password = input("Enter your LinkedIn password: ")

    process = CrawlerProcess({
        'BOT_NAME': 'linkedin_scraper',
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': True,
        'ITEM_PIPELINES': {
            '__main__.LinkedinPipeline': 300,
        }
    })

    process.crawl(LinkedinSpider, 
                 linkedin_email=linkedin_email,
                 linkedin_password=linkedin_password)
    process.start()