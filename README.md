LinkedIn Scraper
This project is a web scraper built using Scrapy and Playwright to extract public profile information from LinkedIn. It collects data such as the profile name, bio, socials, experience, and education.

Features
Scrapes public LinkedIn profiles.
Collects and stores data in CSV format.
Bypasses basic LinkedIn anti-scraping measures using Playwright.
Requirements
Python 3.12+
Scrapy: pip install scrapy
Playwright: pip install playwright
Node.js (Required by Playwright)
Installation
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/your-username/linkedin-scraper.git
cd linkedin-scraper
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
playwright install
Set Up LinkedIn Credentials: Create a .env file with your LinkedIn credentials (use a fake or testing account):

ini
Copy
Edit
LINKEDIN_EMAIL=your-email
LINKEDIN_PASSWORD=your-password
Usage
bash
Copy
Edit
scrapy crawl linkedin_spider
The scraped data will be saved as scraped_output.csv.

Legal Disclaimer
This scraper is intended for educational purposes only. Scraping LinkedIn is against their Terms of Service, and I am not responsible for any misuse of this tool.

Author
Purab Ray
