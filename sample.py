from selenium import webdriver
from selenium.webdriver.common.by import By

# x. Chrome の起動オプションを設定する
options = webdriver.ChromeOptions()
#options.add_argument('--headless')

# x. ブラウザの新規ウィンドウを開く
print('connectiong to remote browser...')
#driver = webdriver.Remote(
#    command_executor='http://localhost:4444/wd/hub',
#    desired_capabilities=options.to_capabilities(),
#    options=options,
#)
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub', 
    options=options
)

driver.get("http://www.google.com")
print(driver.current_url)
# x. ブラウザを終了する
driver.quit()