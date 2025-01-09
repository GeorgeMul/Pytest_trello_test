from selenium import webdriver
from page_services.page_service import Service

driver = webdriver.Firefox()
A = Service(driver)
A.login("https://trello.com/login","lesterjack93@yahoo.com.tw","trello0968141018")
A.into_workspace()
A.create_board("測試用看板")
# A.into_workspace()
# A.delete_board()