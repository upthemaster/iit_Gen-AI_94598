from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from langchain.tools import tool

@tool
def batch_fee_scrape() -> list:
    """
    Scrapes batch schedule and fee details from the Sunbeam internship portal
    and returns structured batch information.
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # fixed source
    driver.get("https://www.sunbeaminfo.in/internship")

    driver.implicitly_wait(10)

    t_base_class = driver.find_element(By.CLASS_NAME, "table-responsive")
    t_css = t_base_class.find_element(By.CSS_SELECTOR, "table.table-bordered.table-striped")
    t_body = t_css.find_element(By.TAG_NAME, "tbody")
    t_row = t_body.find_elements(By.TAG_NAME, "tr")

    internships = []

    for row in t_row:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 7:
            continue

        internships.append({
            "Sr. No.": cols[0].text.strip(),
            "Batch": cols[1].text.strip(),
            "Batch Duration": cols[2].text.strip(),
            "Start Date": cols[3].text.strip(),
            "End Date": cols[4].text.strip(),
            "Time": cols[5].text.strip(),
            "Fees": cols[6].text.strip(),
        })

    driver.quit()
    return internships
