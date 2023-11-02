from selenium import webdriver
from selenium.webdriver.common.by import By
#import chromedriver_binary
#driver = webdriver.Chrome()
options = webdriver.FirefoxOptions()
#driver = webdriver.Firefox(options=options)
driver  = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)

#cService = webdriver.ChromeService(executable_path=
#        '/Users/r-tao/Library/Caches/pip/wheels/51/f7/e4/b5b46fcc294aad82446529cc2b805871999af37787f28d2f75')
#driver = webdriver.Chrome(service = cService)

driver.implicitly_wait(10)

driver.get('https://www.library.chiyoda.tokyo.jp/')

schedule_el = driver.find_elements(
    By.CLASS_NAME,
    'schedule-list01__text'
)

print([s.text for s in schedule_el])
driver.quit()