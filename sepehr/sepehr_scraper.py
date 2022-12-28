import time
import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def click_operation(driver, xpath):
    try:
        time.sleep(5)
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
    except:
        click_operation(driver, xpath)


def send_keys_operations(driver, xpath, keys):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)
    except:
        send_keys_operations(driver, xpath, keys)


def click_drop_down(driver, element1, xpath):
    try:
        element1.click()
        WebDriverWait(driver, .5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except:
        click_drop_down(driver, element1, xpath)


def flight_info_one(driver, xpath):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        result = [x.text for x in driver.find_elements(By.XPATH, xpath)]
    except:
        result = [None]
    return result


def flight_info(driver):
    capacity = flight_info_one(driver, "//div[@class='count iransans-bold-fa-number']")
    price = flight_info_one(driver, "//div[@class='price iransans-medium-fa-number']")
    dep_time = flight_info_one(driver, "//span[@class='departure-time']")
    air_line = flight_info_one(driver, "//span[@class='title']")
    flight_no = flight_info_one(driver, "//span[@class='number iransans-light-fa-number']")
    model = flight_info_one(driver, "//span[@class='airline-name']")
    organization = flight_info_one(driver, "//div[@class='name iransans-light-fa-number']")
    try:
        df = pd.DataFrame({
            'dep_time': dep_time,
            'air_line': air_line,
            'price': price,
            'capacity': capacity,
            'model': model,
            'flight_no': flight_no,
            'organization': organization,
        })
    except:
        flight_info(driver)
    return df


def get_booking_sepehr(data):
    url: str = ("https://sepehr360.ir/")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    driver = webdriver.Chrome("C:\Project\Web Scraping/chromedriver", chrome_options=options)
    driver.get(url=url)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="firstPageSource"]')))
    element1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="firstPageSource"]')))
    click_drop_down(driver, element1, '//*[@id="cdk-overlay-0"]')
    element1.send_keys(data['origin'], Keys.ARROW_DOWN)
    element1.send_keys(Keys.ENTER)
    element1 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="firstPageDestination"]')))
    click_drop_down(driver, element1, '//*[@id="mat-autocomplete-1"]')
    element1.send_keys(data['destination'])
    element1.send_keys(Keys.ENTER)

    # Departure date
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                '//*[@id="home-page-search-box"]/form/div[2]/flight-year-calendar/div/div[2]/shamsi-one-way-date-box/div'))).click()
    list_of_date_elements = driver.find_elements(By.XPATH, '//shamsi-day-calendar//div[@disabled!="true"]')
    list_of_date_elements[0].click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="home-page-search-box"]/form/div[3]/button'))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//*[@id="mainContainer"]/master-container/b2c-oneway-flight-page/header/nav/div/div[2]/top-menu/ul/menu-item[1]/li'))).click()

    list_of_price_date = driver.find_elements(By.XPATH,
                                              "//span[@class='text-center flight-available-price--fontsize iransans-medium-fa-number ng-star-inserted']")
    df = pd.DataFrame()
    for index, value in enumerate(list_of_price_date):
        if isinstance(data['days'],int):
            if index + 1 > data['days']:
                break
        elem1 = list_of_price_date[index]
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(elem1))
        ActionChains(driver).move_to_element(elem1).click(elem1).perform()
        time.sleep(2)

        #We should repeat these two lines of code because in each click the structure of the page changes but the indexes remain the same
        list_of_price_date = driver.find_elements(By.XPATH,
                                                  "//span[@class='text-center flight-available-price--fontsize iransans-medium-fa-number ng-star-inserted']")
        elem1 = list_of_price_date[index]

        try:
            driver.find_element(By.XPATH, '//h4[@class="text-center no-flight-header"]')
            continue
        except:
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="flight-info"]')))
            except:
                continue

            num_of_flights = len(driver.find_elements(By.XPATH, '//div[@class="flight-info"]'))
            df_day = pd.DataFrame({
                'origin': [data['origin']] * num_of_flights,
                'destination': [data['destination']] * num_of_flights,
                'scrap date': [dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * num_of_flights,
                'day': [elem1.find_element(By.XPATH, './ancestor::div[2]').text.split('\n')[1]] * num_of_flights
            })
            if not df.empty:
                df = pd.concat([df, pd.concat([df_day, flight_info(driver)], axis=1)])
            else:
                df = pd.concat([df_day, flight_info(driver)], axis=1)

    return df


# result = get_booking_sepehr(data)
# result.to_excel('test.xlsx')
