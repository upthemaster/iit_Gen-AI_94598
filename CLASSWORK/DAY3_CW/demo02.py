from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# driver is used to control the browser like --> open, close, click, type, navigate
# driver is the bridge between selenius webdriver and browser

driver = webdriver.Chrome()
time.sleep(5)

url = "https://duckduckgo.com/"
driver.get(url)
print("Initial Page Title: ", driver.title)

driver.implicitly_wait(5)
search_box = driver.find_element(By.NAME,"q")

for ch in "dkte college ichalkaranji":
    search_box.send_keys(ch)
    time.sleep(0.2)
search_box.send_keys(Keys.RETURN)

print("Later Page Title:", driver.title)


time.sleep(10)
driver.quit()
