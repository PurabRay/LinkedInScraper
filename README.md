# LinkedIn Scraper

A web scraper built with **Scrapy** and **Playwright** to extract public profile data from LinkedIn. Built as part of my data analysis work at **Undivided Capital**, where the goal was to identify and rank potential early-stage founders for investment consideration.

## What it does

Scrapes public LinkedIn profiles and extracts structured data including name, bio, social links, work experience, and education history. Output is saved to CSV for downstream analysis and ranking.

## Features

- Scrapes public LinkedIn profiles (name, bio, socials, experience, education)
- Saves structured output to `scraped_output.csv`
- Uses Playwright to handle LinkedIn's JavaScript-rendered pages and bypass basic anti-scraping measures
- Handles session management via environment-configured credentials

## Tech Stack

- Python 3.12+
- Scrapy
- Playwright
- python-dotenv

## Setup

```bash
git clone https://github.com/PurabRay/LinkedInScraper.git
cd LinkedInScraper

pip install -r requirements.txt
playwright install
```

Create a `.env` file with LinkedIn credentials (use a test account):
```
LINKEDIN_EMAIL=your-email
LINKEDIN_PASSWORD=your-password
```

## Usage

```bash
scrapy crawl linkedin_spider
```

Output saved to `scraped_output.csv`.

## Context

This was built during my internship at **Undivided Capital** (Feb–May 2025), where I worked on scraping data about potential founders and building ranking algorithms to prioritise investment candidates by favourability. This scraper was one component of that data pipeline.

## Legal Disclaimer

This tool is for educational purposes only. Scraping LinkedIn violates their Terms of Service. Use responsibly and only on profiles you have permission to access.
