from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from langchain.tools import tool

@tool
def web_scrape() -> list:
    """
    web_scrape() tool scrapes the data from the Sunbeam portal.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.sunbeaminfo.in/internship")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    wait = WebDriverWait(driver, 10)
    plus_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
    plus_button.click()

    t_div = driver.find_element(By.ID, "collapseSix")
    t_class = t_div.find_element(By.TAG_NAME, "table")
    t_body = t_class.find_element(By.TAG_NAME, "tbody")
    t_row = t_body.find_elements(By.TAG_NAME, "tr")

    internships = []

    for row in t_row:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 5:
            continue

        internships.append({
            "Technology": cols[0].text.strip(),
            "Aim": cols[1].text.strip(),
            "Prerequisite": cols[2].text.strip(),
            "Learning": cols[3].text.strip(),
            "Location": cols[4].text.strip()
        })

    driver.quit()
    return internships