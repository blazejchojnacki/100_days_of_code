from selenium import webdriver
from selenium.webdriver.common.by import By

browser_options = webdriver.EdgeOptions()
browser_options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=browser_options)
driver.get('https://www.python.org/')

final_dict = {}
# element_div = driver.find_element(By.CLASS_NAME, value="medium-widget event-widget last")
result_list = driver.find_elements(By.CSS_SELECTOR, value=".event-widget li")
for element in result_list:
    data = {'time': element.find_element(By.CSS_SELECTOR, value='time').text,
            'name': element.find_element(By.CSS_SELECTOR, value='a').text}
    final_dict[result_list.index(element)] = data

driver.close()
# driver.quit()

print(final_dict)
