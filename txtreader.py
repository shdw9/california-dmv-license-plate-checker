from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from colorama import Fore, init
import os
import warnings
#import discord #doesn't use discord
from discord.ext import commands
import time
from time import sleep

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

driver = webdriver.Chrome(ChromeDriverManager(version='91.0.4472.101').install(), options=options)
os.system('cls')

def check(plate):
    if (len(plate) > 7):
        print("")
        return
    driver.get("https://www.dmv.ca.gov/wasapp/ipp2/initPers.do")
    sleep(2)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div[1]/fieldset/ul/li/label").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div[2]/button").click()
    sleep(1)
    driver.find_element_by_xpath("//select[@name='vehicleType']/option[text()='Auto']").click()
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[2]/input").send_keys(beingreplaced)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[4]/input").send_keys(last3vin)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[5]/div[2]/label").click()
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[6]/div[2]/label").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/fieldset/div[8]/div[1]/div[4]/div/div/label").click()
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div/button").click()
    sleep(2)
    i = 0
    for element in plate:
        driver.find_element_by_id("plateChar" + str(i)).send_keys(element)
        i += 1
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div[2]/button").click()
    sleep(2)
    try:
        if (driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/div[1]/div[2]")):
            print("")
            return False
    except:
        pass
    try:
        if ("502 ERROR" in driver.find_element_by_xpath("/html/body/h1").text):
            check(plate)
    except:
        pass
    try:
        if(driver.find_element_by_xpath("/html/body/div[3]/div/main/div[2]/div[2]/form/div[1]/dl/dd[1]/div/img")):
            print("AVAILABLE!")
            return True
    except:
        pass

file2 = open('availablenames.txt', 'a')
file2.write("--------------------------\n")
file2.close()
file1 = open('names.txt', 'r')

count = 0
 
print("Now checking license plates ...")

for line in file1:
    file2 = open('availablenames.txt', 'a')
    count += 1
    print(line.strip(), end = "\t")
    try:
        if(check(line.strip())):
            file2.write(line.strip() + "\n")
    except:
        pass

 
# Closing files 
file1.close()
print(" >> fin")
