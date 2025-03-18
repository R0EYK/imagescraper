from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# --- Chrome Options for Speed ---
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Disable images, CSS, fonts
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
    "profile.managed_default_content_settings.fonts": 2
}
options.add_experimental_option("prefs", prefs)

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# --- Website Details ---
BASE_URL = "https://gallery.tagbox.co.il/gallery/uzTruz0QM7G3fjSqT2I5/photos/"
TOTAL_PAGES = 94
BASE_DOMAIN = "https://gallery.tagbox.co.il"

for page in range(1, TOTAL_PAGES + 1):
    print(f"Processing page {page}/{TOTAL_PAGES}...")

    driver.get(f"{BASE_URL}{page}")

    # Wait for image links to load
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[class*='MuiBox-root css-']"))
        )
    except:
        print(f"No images found on page {page}")
        continue

    # Collect image URLs to avoid stale element issues
    image_links = driver.find_elements(By.CSS_SELECTOR, "a[class*='MuiBox-root css-']")
    image_urls = [img_link.get_attribute("href") for img_link in image_links]

    for img_page_url in image_urls:
        if not img_page_url.startswith("http"):
            img_page_url = BASE_DOMAIN + img_page_url

        driver.get(img_page_url)

        try:
            # Wait for Download button to appear and click
            download_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Download')]"))
            )
            download_button.click()
            print(f"Downloaded image: {img_page_url}")

           

        except:
            print(f"Download button not found on {img_page_url}")

        # Go back to gallery page
        driver.back()

        # Wait for gallery page to load again before continuing
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[class*='MuiBox-root css-']"))
            )
        except:
            print(f"Gallery page failed to reload after visiting {img_page_url}")

driver.quit()
print("✅ All done!")
