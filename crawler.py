from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pprint

url = "https://emap.pcsc.com.tw/"

# Store data of all 7-11 stores in Taiwan
data = {}

driver = webdriver.Chrome()
driver.get(url)

# Button to home page
home = driver.find_element(By.ID, "link_reset")

# All cities in Taiwan
cities = driver.find_elements("xpath", "//a[@href]")
cities = cities[5:7]

for city in cities:
    data[city.get_attribute("innerHTML")] = {}
    city.click()
    time.sleep(2)
    
    # Districts of a city
    districts = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@id='counties_s_li' and @title='countrieslist'][count(.//a)>0]//a"))
    )
    
    for i in range(0, len(districts)):
        data[city.get_attribute("innerHTML")][districts[i].get_attribute("innerHTML")] = {}
        
        districts[i].click()
        time.sleep(3)
        
        # Roads of a district
        roads = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@id, 'section_')]"))
        )
        
        # Button to the city
        back_to_city = driver.find_element(By.ID, "map_all_link1")
        
        for j in range(0, len(roads)):
            data[city.get_attribute("innerHTML")][districts[i].get_attribute("innerHTML")][roads[j].get_attribute("innerHTML")] = []
        
        back_to_city.click()
        time.sleep(2)
        
        # Reload districts since DOM data will disappear
        districts = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@id='counties_s_li' and @title='countrieslist'][count(.//a)>0]//a"))
        )
    
    home.click()
    time.sleep(2)
    
pprint.pprint(data)