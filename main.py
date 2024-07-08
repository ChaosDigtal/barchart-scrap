from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
#options.add_argument('--headless=new')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)

driver.get('https://barchart.com/login')

print("Iputing email")

email = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.XPATH, f"//input[@name='email']")))
email.send_keys('scottmgoley@gmail.com')

print("Inputing password")

password = driver.find_element(By.NAME, 'password')
password.send_keys('Upwork123')

print("Clicking login button")

btn_login = WebDriverWait(driver, 5) \
                            .until(EC.element_to_be_clickable(
                            (By.XPATH, f"//button[@class='bc-button login-button']")))
btn_login.click()



