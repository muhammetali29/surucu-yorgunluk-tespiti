from selenium import webdriver
import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

def scrape_images(search_engine, query, num_images, save_path):

    if search_engine == "google":
        search_url = f"https://www.google.com/search?q={query}&tbm=isch"
        img_selector = "img.Q4LuWd"
        full_img_selector = 'img.sFlh5c.pT0Scc.iPVvYb'
    elif search_engine == "bing":
        search_url = f"https://www.bing.com/images/search?q={query}"
        img_selector = "img.mimg"
        full_img_selector = 'img.nofocus'
    elif search_engine == "yandex":
        search_url = f"https://yandex.com/images/search?text={query}"
        img_selector = "div.serp-item img"
        full_img_selector = 'img.MMImage-Origin'
    else:
        raise ValueError("Unsupported search engine. Choose 'google', 'bing', or 'yandex'.")

    driver.get(search_url)

    for _ in range(num_images // 50):
        driver.execute_script("window.scrollBy(0,10000)")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, img_selector)))

    img_elements = driver.find_elements(By.CSS_SELECTOR, img_selector)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    save_path = os.path.join(desktop_path, save_path)
    os.makedirs(save_path, exist_ok=True)

    for i, img_element in enumerate(img_elements[:num_images]):
        try:
            img_element.click()


            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, full_img_selector)))

            img_url_element = driver.find_element(By.CSS_SELECTOR, full_img_selector)
            img_url = img_url_element.get_attribute("src")

            img_name = f"{query.replace(' ', '_')}_{i+1}.jpg"
            img_path = os.path.join(save_path, img_name)
            response = requests.get(img_url, stream=True)
            with open(img_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"Image {i+1} downloaded successfully")

        except Exception as e:
            print(f"Failed to download image {i+1}: {e}")

queries = [
    "driver fatigue signs",
    "tired driver face",
    "sleepy eyes driving",
    "yawning driver",
    "driver micro-sleep"
]

num_images_per_query = 200

search_engines = ["google", "bing", "yandex"]

for search_engine in search_engines:
    for query in queries:
        print(f"Downloading images for query: {query} from {search_engine}")
        scrape_images(search_engine, query, num_images_per_query, f"{search_engine}_{query}")

driver.quit()
