from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import shutil
import time
import os

# Define the download directory
home_directory = os.path.expanduser("~")
download_directory = os.path.join(home_directory, "barchart")

# Clear the download directory if it exists
if os.path.exists(download_directory):
    shutil.rmtree(download_directory)
os.makedirs(download_directory)

options = Options()
#options.add_argument('--headless=new')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('prefs', {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True  # To enable downloading
})

# Set up the ChromeDriver
driver = webdriver.Chrome(options=options)

driver.get('https://barchart.com/login')

print("Iputing email")

email = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.XPATH, f"//input[@name='email']")))
email.send_keys('scottmgoley@gmail.com')

print("Inputing password")

password = driver.find_element(By.NAME, 'password')
password.send_keys('Upwork123')

print("Clicking login button")

btn_login = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"//button[@class='bc-button login-button']")))
btn_login.click()

print("accessing industry-rankings page")
driver.get('https://www.barchart.com/stocks/sectors/industry-rankings?page=all')

print("downloading industry-rankings")
download = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"//a[@class='toolbar-button download ng-isolate-scope']")))
download.click()

time.sleep(1)

scroll_pause_time = 3  # Pause time between scrolls (seconds)
screen_height = driver.execute_script("return window.innerHeight")  # Get the height of the screen
overlap = 0.5  # Fraction of the screen height to overlap

scroll_amount = int(screen_height * (1 - overlap))  # Calculate the amount to scroll each time
while True:
    # Scroll down by the calculated amount
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_amount)
    
    # Wait for the new content to load
    time.sleep(scroll_pause_time)
    
    # Check if we've reached the bottom of the page
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight")
    if scroll_position >= scroll_height:
        break


# Find the shadow host element and extract a_tags inside shadow DOM
try:
    # Find all a tags within the shadow DOM
    a_tags = driver.execute_script("""return document.querySelector('bc-data-grid').shadowRoot.querySelectorAll('a[href^="/stocks/quotes/"]')""")
    # Extract and print the href attributes
    links = set()
    for a_tag in a_tags:
        href = a_tag.get_attribute('href')
        #if href and "/stocks/quotes/" in href:
        links.add(href)
    
    # Print the unique links
    for link in links:
        driver.get(str.replace(link, "components", "historical-download"))
        download = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"//a[@class='bc-button add light-blue download-btn ng-isolate-scope']")))
        download.click()
        time.sleep(2)

except Exception as e:
    print(f"An error occurred: {e}")



