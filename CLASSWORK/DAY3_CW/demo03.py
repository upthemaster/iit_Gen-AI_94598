from selenium import webdriver
from selenium.webdriver.common.by import By  # common is reusable selenium component used across different webdriver features
from selenium.webdriver.chrome.options import Options

# - - - N O T E S - - -

# chrome_options sets the setting for the chrome browser
# headless means without UI
# in add_argument we pass the rules to the chrome before it get opens

chrome_options = Options() # option is an object which is used to store the browser configuration setting
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://nilesh-g.github.io/learn-web/HTML/demo08.html")
print("Page Title:", driver.title)

driver.implicitly_wait(5)

list_items = driver.find_elements(By.TAG_NAME, "li")

for item in list_items:
    print(item.text)

driver.quit()
