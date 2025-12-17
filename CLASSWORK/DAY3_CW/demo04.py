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

table_body = driver.find_element(By.TAG_NAME, "tbody")
table_rows = table_body.find_elements(By.TAG_NAME, "tr")
for row in table_rows:
    # print(row.text)
    cols = row.find_elements(By.TAG_NAME, "td")
    info = {
        "sr": cols[0].text,
        "title": cols[1].text,
        "author": cols[2].text,
        "category": cols[3].text,
        "price": cols[4].text
    }
    print(info)

driver.quit()
