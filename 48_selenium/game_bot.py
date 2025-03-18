from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time
# import datetime

browser_options = webdriver.EdgeOptions()
browser_options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=browser_options)
driver.get('http://orteil.dashnet.org/experiments/cookie/')

cookie = driver.find_element(By.ID, value='cookie')
# store_divs = driver.find_element(By.ID, value='store').find_elements(By.TAG_NAME, value='div')
upgrade_thresholds = {key: -1 for key in range(8)}


def check_upgrade():
    # global store_divs
    store_divs = [_ for _ in driver.find_elements(By.CSS_SELECTOR, value='#store div')
                  if _.get_attribute('class') != 'amount']
    try:
        for index in range(-len(store_divs) + 2, 1):
            if upgrade_thresholds[-index] < 0:
                if threshold_text := store_divs[-index].text:
                    threshold_value = int(''.join(threshold_text.split('\n')[0].split(' - ')[1].split(',')))
                    if threshold_value <= int(driver.find_element(By.ID, value='money').text):
                        store_divs[-index].click()
                        break
                    else:
                        upgrade_thresholds[-index] = threshold_value
            else:  # if -index in upgrade_thresholds:
                if upgrade_thresholds[-index] <= int(driver.find_element(By.ID, value='money').text):
                    store_divs[-index].click()
                    upgrade_thresholds[-index] = -1
                    break
    except StaleElementReferenceException:
        check_upgrade()


def get_time(interval=0):
    # current_time = datetime.datetime.now()
    # current_value = int(current_time.minute * 60 + current_time.second) + interval
    current_value = time.time() + interval
    return current_value


for n in range(60):
    end_value = get_time(interval=5)
    while end_value >= get_time():
        cookie.click()
    check_upgrade()

print('end')
