import undetected_chromedriver as uc
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_linkedin(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 20)
    
    # Wait for the username field and fill in credentials
    email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    email_field.clear()
    email_field.send_keys(email)
    
    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys(password)
    
    # Click the login button
    sign_in_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    sign_in_button.click()
    
    # Wait for a known post-login element (for example, the search bar or nav element)
    wait.until(EC.presence_of_element_located((By.ID, "global-nav-search")))
    print("Login successful.")

def scrape_profile(driver, url):
    driver.get(url)
    # Wait for page to load and scroll to trigger lazy loading
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(2)
    
    # Extract profile information
    wait = WebDriverWait(driver, 15)
    try:
        name = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.text-heading-xlarge")
        )).text.strip()
    except Exception:
        name = ""
    
    try:
        bio = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text.strip()
    except Exception:
        bio = ""
    
    # Try to extract socials from the Contact Info popup
    socials = []
    try:
        contact_button = driver.find_element(By.CSS_SELECTOR, "a.pv-contact-info__contact-link")
        contact_button.click()
        time.sleep(2)
        social_elements = driver.find_elements(By.CSS_SELECTOR, "section.pv-contact-info a")
        for elem in social_elements:
            href = elem.get_attribute("href")
            if href and any(domain in href for domain in 
                           ["twitter.com", "github.com", "facebook.com", "instagram.com", "youtube.com"]):
                socials.append(href)
    except Exception:
        pass  # Contact info might not be available
    
    # Placeholder for experience and education extraction
    experience = []  # You can add more refined extraction here
    education = []   # Likewise, adjust as needed

    return {
        "linkedin_url": url,
        "name": name,
        "bio": bio,
        "socials": socials,
        "experience": experience,
        "education": education
    }

def main():
    linkedin_email = input("Enter your LinkedIn email: ")
    linkedin_password = input("Enter your LinkedIn password: ")
    
    # Load LinkedIn profile URLs from your Excel file (expects a column "LinkedIn URLs")
    try:
        df = pd.read_excel("Assignment.xlsx")
        urls = df["LinkedIn URLs"].tolist()
    except Exception as e:
        print("Error reading Excel file:", e)
        return
    
    # Set up undetected-chromedriver in headful mode (to mimic real user behavior)
    options = uc.ChromeOptions()
    options.headless = False  # Running in headful mode is less likely to be flagged
    options.add_argument("--window-size=1280,800")
    # You can add proxy arguments here if needed
    driver = uc.Chrome(options=options)
    
    try:
        login_linkedin(driver, linkedin_email, linkedin_password)
        scraped_data = []
        for url in urls:
            print("Scraping:", url)
            data = scrape_profile(driver, url)
            scraped_data.append(data)
            # Random delay to mimic human behavior
            time.sleep(3)
        
        # Save output to CSV
        output_df = pd.DataFrame(scraped_data)
        output_df.to_csv("scraped_output.csv", index=False)
        print("Scraping completed. Output saved to scraped_output.csv")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
