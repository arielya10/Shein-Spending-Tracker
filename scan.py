import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from forex_python.converter import CurrencyRates
import time

def Driver(browser):
    if browser == 'firefox':
        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages', 'en-US, en')
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),firefox_profile=profile)
    else:
        driver = uc.Chrome()
    return driver

def set_lang(driver):
    driver.get('https://www.shein.com/user/orders/list?from=navTop')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div/div/div[1]/span')))
    Actionchains = ActionChains(driver)
    Actionchains.move_to_element(driver.find_element(By.XPATH,'/html/body/div[1]/header/div[2]/div[1]/div/div[1]/div/div[3]/div[5]/a')).perform()
    driver.find_element(By.XPATH,'/html/body/div[1]/header/div[2]/div[1]/div/div[1]/div/div[3]/div[5]/div/div[4]/a[2]').click()
    time.sleep(1)
    return driver

def login(url,user,pas,driver):
    driver.get(url)
    time.sleep(2)
    try:
        driver.find_element(By.XPATH,'/html/body/div[5]/div/div[3]/div/div/div[1]/i').click()
    except Exception:
        print()
    email = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div/div[3]/div[1]/div/div/input')
    email.clear()
    email.send_keys(user)
    password = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div/div[3]/div[2]/div/div/input')
    password.clear()
    password.send_keys(pas)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div/div[3]/div[4]/button').click()
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div/div[1]/div/div[1]/h4/span')))
    except Exception:
        print("The Email Address or Password you entered is incorrect.")
        exit(1)
    return driver

def scrape(driver):
    page = 3
    i=1
    counter=0
    total_price = 0
    driver = set_lang(driver)
    while True:
        try:
            status = driver.find_element(By.XPATH,f'/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/ul[2]/li[{i}]/div[2]/div[4]/div/div[1]/span').text
            if status == 'Shipped' or status == 'Delivered':
                #Getting item price
                order = driver.find_element(By.XPATH,f'/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/ul[2]/li[{i}]/div[2]/div[2]/span').text
                #Checking currency
                if '₪' in order:
                    order = order.replace('₪', '')
                    price=float(order)
                    price = cr.convert('ILS', 'USD', price)
                else:
                    order = order.replace('$', '')
                    price=float(order)
                counter+=1
                total_price+=price
                print(f"Price: {price:.2f}$, (order number: {counter})\n")
            i+=1
        except Exception:
            try:
                driver.find_element(By.XPATH,f'/html/body/div[1]/div[1]/div[1]/div[2]/div[5]/div/nav/span[{page}]').click()
                page+=1
                time.sleep(2)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/div[1]')))
                i=1
            except Exception:
                break
    print(f"Total money spent: {total_price:.2f}$\n")
    print(f"{counter} orders...\n")

if __name__ == '__main__':
    cr = CurrencyRates()
    parser = argparse.ArgumentParser(description='Calculate spent money on Shein')
    parser.add_argument('-u','--user',type=str,help='Account email')
    parser.add_argument('-p', '--password', type=str, help='Account password')
    parser.add_argument('-b', '--browser', type=str, help='browser to use (firefox or chrome',default='chrome')
    args = parser.parse_args()
    url = 'https://www.shein.com/user/auth/login?direction=nav&from=navTop'
    driver= Driver(args.browser)
    driver = login(url,args.user,args.password,driver)
    scrape(driver)


