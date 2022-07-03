from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from colorama import Fore, init
import os
import warnings
import time

init()
init(convert=True)

beingreplaced = "8JBZ269"
last3vin = "695"

warnings.filterwarnings("ignore", category=DeprecationWarning)
options = Options()
options.headless = True
options.add_argument("--log-level=3")
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
os.system('cls')

def check(arg):
    if len(arg) > 7:
        print("License plates must be <= 7 characters")
        return
        
    driver.get("https://www.dmv.ca.gov/wasapp/ipp2/initPers.do")
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div[1]/fieldset/ul/li/label").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div[2]/button").click()
    time.sleep(1)
    driver.find_element_by_xpath("//select[@name='vehicleType']/option[text()='Auto']").click()
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[2]/input").send_keys(beingreplaced)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[4]/input").send_keys(last3vin)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[5]/div[2]/label").click()
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[6]/div[2]/label").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[8]/div[1]/div[4]/div/div/label").click()
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div/button").click()
    time.sleep(2)
    i = 0
    for element in arg:
        driver.find_element_by_id("plateChar" + str(i)).send_keys(element)
        i += 1
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div[2]/button").click()
    time.sleep(2)
    try:
        if (driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/div[1]/div[2]")):
            print("The license plate " + arg + " is NOT available!")
            pass
    except:
        pass
    try:
        if ("502 ERROR" in driver.find_element_by_xpath("/html/body/h1").text):
            print("BOT IS BLOCKED MY DMV.CA.GOV")
    except:
        pass
    try:
        if(driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div[1]/dl/dd[1]/div/img")):
            print("The license plate " + arg + " is available!")
            print(driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div[1]/dl/dd[1]/div/img").get_attribute("src"))
            pass
    except:
        pass

while(True):
    a = input("\nEnter a license plate: ")
    if a.lower() == "stop":
        break
    print("Checking if " + a + " is available ...")
    check(a)
