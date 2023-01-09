from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import re


def click_operation(driver, xpath):
    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element.click()
    except:
        click_operation(driver, xpath)


def send_keys_operations(driver, xpath, keys):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)
    except:
        send_keys_operations(driver, xpath, keys)


def get_booking_page(data):
    # Create logger and assign handler
    logging.basicConfig(filename='log.log', filemode='a', format="%(asctime)s|%(levelname)s|%(name)s|%(message)s")
    logger = logging.getLogger("guru")
    # handler = logging.FileHandler('log.log')
    # handler.setFormatter(logging.Formatter())
    # logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info('Application started.')
    url: str = ("https://www.flygp.se/guru2/v3.5/")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    driver = webdriver.Chrome("G:\Python projects\Pazh/chromedriver", chrome_options=options)
    driver.get(url=url)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="ErrorCatching-app"]/div[1]/div/div[1]/div[1]/div[2]/input')))
    compBox = driver.find_element(By.XPATH, '//*[@id="ErrorCatching-app"]/div[1]/div/div[1]/div[1]/div[2]/input')
    compBox.send_keys('shi')
    loginBox = driver.find_element(By.XPATH, '//*[@id="ErrorCatching-app"]/div[1]/div/div[1]/div[2]/div[2]/input')
    loginBox.send_keys('mike.tango')
    passBox = driver.find_element(By.XPATH, '//*[@id="ErrorCatching-app"]/div[1]/div/div[1]/div[3]/div[2]/input')
    passBox.send_keys('09125820385')
    click_operation(driver, '//*[@id="ErrorCatching-app"]/div[1]/div/div[2]/button')

    logger.info('Logged in.')

    click_operation(driver, '/html/body/div[3]/div[3]/div/div[3]/button/span')
    click_operation(driver, '//*[@id="clickDiv"]')
    click_operation(driver, '//*[@id="ErrorCatching-app"]/div/div/div/button/span')
    # flight no
    stringBox = driver.find_element(By.XPATH, '//*[@id="flightNo"]')
    stringBox.send_keys(data['flight_no'])
    # flight ADEP
    stringBox = driver.find_element(By.XPATH, '//*[@id="adep"]')
    stringBox.send_keys(data['ADEP'])
    # flight STD
    stringBox = driver.find_element(By.XPATH, '//*[@id="std"]')
    stringBox.send_keys(data['STD'])
    # flight Tail-ID
    click_operation(driver, '//*[@id="ErrorCatching-app"]/div/div/div/div[1]/form/div/div[2]/div/div/div')
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f'//li[contains(text(), "{data["Tail_id"]}")]'))).click()
    # flight ADES
    stringBox = driver.find_element(By.XPATH, '//*[@id="ades"]')
    stringBox.send_keys(data['ADES'])
    # flight STA
    stringBox = driver.find_element(By.XPATH, '//*[@id="sta"]')
    stringBox.send_keys(data['STA'])
    click_operation(driver, '//*[@id="ErrorCatching-app"]/div/div/div/div[1]/form/div/div[8]/button[2]/span')

    logger.info('First page params are filled and create button clicked.')

    if data['UseMETAR']:
        click_operation(driver, '//*[@id="123123"]')
    else:
        send_keys_operations(driver, '//*[@id="windInput"]', data['WindDirec'] + '/0' + data['WindSpeed'])
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="oat"]'))).send_keys(data['OAT'])
        # click QNH inHg
        click_operation(driver,
                        '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[1]/div[3]/div[2]/div')
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[contains(text(), "inHg")]'))).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="qnh"]'))).send_keys(
            int(re.split(r'(\d+)', data['QNH'])[1]) / 100)

        # click Runway
        click_operation(driver,
                        '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div/div[2]/form/div[1]/div[2]/div/div')
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[contains(text(), "{data["Runway"]}")]'))).click()
        # click Flaps
        click_operation(driver,
                        '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div/div[2]/form/div[2]/div[1]/div[1]/div/div/div')
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[contains(text(), "{data["Flaps"]}")]'))).click()
        # click AntiIce
        click_operation(driver,
                        '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div/div[2]/form/div[2]/div[1]/div[2]/div/div/div')
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[contains(text(), "{data["AntiIce"]}")]'))).click()
        # click Packs
        click_operation(driver,
                        '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div/div[2]/form/div[2]/div[1]/div[3]/div/div/div')
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[contains(text(), "{data["Packs"]}")]'))).click()
        # click Improved
        click_operation(driver,
                        '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div/div[2]/form/div[2]/div[1]/div[4]/div/div/div')
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[contains(text(), "{data["Improved"]}")]'))).click()
        logger.info('Second page params are filled and create button clicked.')

    # click Runways tab
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="mass"]'))).send_keys('0')
    click_operation(driver, '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[2]/button[2]/span')
    logger.info('Runways button clicked.')

    WebDriverWait(driver, 120).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div[2]/header/div/div[1]/button')))
    logger.info('Add NOTAM button is clickable.')

    not_empty = True
    i = 0
    result_list = []
    while not_empty:
        i += 1
        try:
            result_list.append(driver.find_element(By.XPATH,
                                                   f'//*[@id="ErrorCatching-app"]/div/div/div[2]/div[3]/div[2]/nav/div[{i}]').text.split(
                '\n'))
        except Exception as e:
            not_empty = False
            # logger.error(f'Error occured while reading row {i} the table and error is: {e}.')
    logger.info('Result is ready and process finished.')
    result1 = []
    for l in result_list:
        dict1 = {
                'BandNo': l[0],
                'Feet': l[1],
                'Weight': l[2]
            }
        result1.append(dict1)
    result = {'GetAllCrudRobotsResponseItemViewModels':result1}
    return result

# result = get_booking_page('THR', 'AWZ', 1, 0, 0, '1401-10-01', '1401-10-02')
# print(result)
