from selenium import webdriver
import os
import time
import requests
from selenium.webdriver.common.by import By

# Replace with the path to your ChromeDriver executable
DRIVER_PATH = r'chromedriver.exe'

# Search term and URL
search_query = 'Dog'  # Change this to your desired search query
url = f'https://www.google.com/search?q={search_query}&tbm=isch'

# Create a folder to store downloaded images
os.makedirs(search_query, exist_ok=True)

# Configure Chrome options to automatically download images to the specified folder
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': os.path.abspath(search_query)}
chrome_options.add_experimental_option('prefs', prefs)

# Initialize Chrome WebDriver
with webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options) as driver:
    # Open Google Images
    driver.get(url)
    time.sleep(3)  # Allow time for the page to load

    # Scroll to load more images (change the range for more or fewer images)
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Let the new images load

    # Find image elements
    images = driver.find_elements(By.CSS_SELECTOR, 'img.Q4LuWd')

    # Download images
    downloaded_count = 0
    for index, image in enumerate(images):
        if downloaded_count >= 50:  # Download at most 50 images
            break

        image_url = image.get_attribute('src')
        if image_url:
            try:
                # Download the image
                img_data = requests.get(image_url).content
                img_name = f'{search_query}/{search_query}_{index}.jpg'
                with open(img_name, 'wb') as img_file:
                    img_file.write(img_data)
                    downloaded_count += 1
                    print(f"Downloaded image {downloaded_count}")
            except Exception as e:
                print(f"Failed to download image: {str(e)}")

print("Image download completed.")
