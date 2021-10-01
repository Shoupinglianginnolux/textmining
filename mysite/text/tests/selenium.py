from selenium import chromedriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

browser = webdriver.Chrome() 
browser.get("http://127.0.0.1:8000/crpd/test/")
assert "Computer Risk Prediction System" in driver.title
elem = browser.find_element_by_id("defect_classification_navbar")
elem.click()
assert "http://127.0.0.1:8000/crpd/test/" in driver.page_source
driver.close()