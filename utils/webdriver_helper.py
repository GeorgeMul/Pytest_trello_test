from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class driver_helper:
    
    def __init__(self,driver):
        self.driver = driver
    
    def get_page(self,URL):
        self.driver.get(URL)
    
    def find_ele(self,xpath):
        return self.driver.find_element(By.XPATH,xpath)
    
    def find_ele_after_present(self,timelimit,xpath):
        return WebDriverWait(self.driver, timelimit).until(
    EC.presence_of_element_located((By.XPATH, xpath))
)
    
    def find_ele_after_visible(self,timelimit,xpath):
        return WebDriverWait(self.driver, timelimit).until(
    EC.visibility_of_element_located((By.XPATH, xpath))
)
    
    def find_ele_after_clickable(self,timelimit,xpath):
        return WebDriverWait(self.driver, timelimit).until(
    EC.element_to_be_clickable((By.XPATH, xpath))
)

