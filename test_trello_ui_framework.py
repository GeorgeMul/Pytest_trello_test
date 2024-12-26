from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#--------------------------------------------------------------------------------------------------------------------------------
#定位器
trello_page_locator = {  #這是本地的locator，已同步完畢
    #選擇工作區的菜單
    'workspace_switcher':'//*[contains(@data-testid,"workspace-switcher")]',
    #進入選擇的工作區
    'into_workspace':'//*[contains(@data-testid,"workspace-switcher-popover-tile")]//*[contains(normalize-space(),"萊斯特")]',
    #看板們
    'boards':'//*[contains(@class,"cZx7p8hAQGLEz5 l7ix_KdG4LuugK")]',
    #工作區進入看板的按鈕
    'workspace_into_board':'//*[contains(@title,"測試用看板")and contains(@class,"hPB1MFHtrhA_in")]',
    #看板旁邊三個點點的按鈕
    'board_overflow_menu':'//*[contains(@title,"測試用看板")]/following-sibling::*//*[contains(@data-testid,"OverflowMenuHorizontalIcon")]',
    #關閉或離開看板按鈕
    'close_board':'//*[contains(@data-testid,"ForwardIcon")]',
    #確認關閉看板按鈕
    'confirm_close_board':'//button[contains(@data-testid,"popover-close-board-confirm")]',
    #查看已關閉的看板
    'check_closed_board':'//footer[contains(@class,"vccO4XHqldnulB")]//button',
    #刪除面板
    'delete_board':'//*[contains(@class,"KIigWC5xzGtpZ7")and contains(normalize-space(),"測試用看板")]//button[contains(@data-testid,"close-board-delete-board-button")]',
    #確認刪除面板
    'delete_board_confirm':'//button[contains(@data-testid,"close-board-delete-board-confirm-button")]',
    #離開關閉看板展示頁面
    'leave_closed_board':'//button//*[contains(@data-testid,"CloseIcon")]',
    #創建看板按鈕
    'create_board_button':'//button[contains(@data-testid,"create-board-tile")]',
    #看板名稱輸入欄位
    'input_board_title':'//input[contains(@data-testid,"create-board-title-input")]',
    #確認創建看板按鈕
    'create_board_submit':'//button[contains(@data-testid,"create-board-submit-button")]',
    #創建列表按鈕
    'create_list_button':'//button[contains(@data-testid,"list-composer")]',
    #新列表名稱輸入欄位
    'new_listname_input':'//textarea[contains(@class,"oe8RymzptORQ7h")]',
    #確認創建列表
    'create_list_submit':'//button[contains(@data-testid,"list-composer-add")]',
    #列表三個點點按鈕
    'list_overflow_menu':'//*[contains(normalize-space(),"測試用列表")]/following-sibling::*//*[contains(@data-testid,"list-edit-menu-button")]',
    #列表封存按鈕
    'archive_list_button':'//button[contains(@data-testid,"list-actions-archive")]',
    #看板內右上角三個點點按鈕
    'overflow_menu_inboard':'//button[contains(@class,"GDunJzzgFqQY_3 frrHNIWnTojsww bxgKMAm3lq5BpA HAVwIqCeMHpVKh SEj5vUdI3VvxDc")]',
    #查看已封存的項目
    'check_archived':'//button//*[contains(@data-testid,"ArchiveIcon")]',
    #切換卡片/列表
    'archived-switcher':'//*[contains(@class,"archive-controls-switch")]',
    #刪除列表
    'delete_list':'//*[contains(normalize-space(),"測試用列表")]/following-sibling::*//*[contains(@class,"button-link js-delete")]',
    #確認刪除按鈕
    'delete_confirm':'//*[contains(@data-testid,"popover-confirm")]',
    #新增卡片按鈕
    'create_card_bUtton':'//*[contains(normalize-space(),"測試用列表")]/following-sibling::*//button[contains(@data-testid,"list-add")]',
    #新卡片名稱輸入欄位
    'new_cardname_input':'//textarea[contains(@data-testid,"list-card")]',
    #確認新增卡片
    'create_card_submit':'//button[contains(@data-testid,"list-card-composer-add")]',
    #快捷編輯卡片按鈕(滑鼠放上去才可見)
    'card-editor':'//*[contains(@data-testid,"trello-card")and contains(normalize-space(),"測試用卡片")]//*[contains(@data-testid,"quick-card-editor-button")]',
    #卡片按鈕
    'card-button':'//*[contains(@data-testid,"trello-card")and contains(normalize-space(),"測試用卡片")]',
    #封存卡片按鈕
    'card-archive-button':'//button[contains(@data-testid,"archive")]',
    #刪除卡片按鈕
    'card-delete-button':'//button[contains(@data-testid,"delete")]',
    #新增描述按鈕
    'add_description_button':'//button[contains(@class,"krMmYdD0ayf5Qo")]',
    #卡片描述輸入欄位
    'card_description_textarea':'//*[contains(@id,"ak")]',
    #儲存描述按鈕
    'description_save_button':'//*[contains(@data-testid,"description-save")]',
    #卡片描述的文字
    'card_description':'//*[contains(@class,"ak-renderer-doc")]',
    #新增checklist按鈕
    'create_checklist_button':'//button[contains(@data-testid,"checklist")]',
    #確認新增checklist
    'create_checklist_submit':'//button[contains(@class,"HwRbvTPVxzo9OE bxgKMAm3lq5BpA SEj5vUdI3VvxDc")]'
    
}

#-------------------------------------------------------------------------------------------------------------
#element會用到的功能
class driver_helper:
    
    def __init__(self,driver):
        self.driver = driver
    
    def get_page(self,URL):
        self.driver.get(URL)
    
    def find_ele(self,xpath):
        return self.driver.find_element(By.XPATH,xpath)
    
    def find_ele_after_present(self,timelimit,xpath):
        return WebDriverWait(self.driver, timelimit).until(
    EC.presence_of_element_located((By.XPATH, xpath))
)
    
    def find_ele_after_visible(self,timelimit,xpath):
        return WebDriverWait(self.driver, timelimit).until(
    EC.visibility_of_element_located((By.XPATH, xpath))
)
    
    def find_ele_after_clickable(self,timelimit,xpath):
        return WebDriverWait(self.driver, timelimit).until(
    EC.element_to_be_clickable((By.XPATH, xpath))
)
    
    def find_ele_after_located(self,timelimit,xpath):
        return WebDriverWait(self.driver, timelimit).until(
    EC.presence_of_all_elements_located((By.XPATH, xpath))
)


#-------------------------------------------------------------------------------------------------------------------
#登入    

def login(driver,URL,email,pwd):
    A = driver_helper(driver)
    A.get_page(URL)
    input_email = A.find_ele_after_present(10,'//*[@id="username"]')
    input_email.send_keys(email)
    submit = A.find_ele('//*[@id="login-submit"]/span')
    submit.click()
    input_pwd = A.find_ele_after_visible(10,'//*[@id="password"]')
    input_pwd.send_keys(pwd)
    submit.click()

#-------------------------------------------------------------------------------------------------------------------
driver = webdriver.Firefox()
mouse = ActionChains(driver)

login(driver,"https://trello.com/login","lesterjack93@yahoo.com.tw","trello2097518")

A = driver_helper(driver)

into_workspace = A.find_ele_after_clickable(10,trello_page_locator['workspace_switcher'])
into_workspace.click()

into_workspace = A.find_ele_after_clickable(10,trello_page_locator['into_workspace'])
into_workspace.click()

board_list = A.find_ele_after_located(10,trello_page_locator['boards'])
board_names = [board.text for board in board_list]

finish_test = False
if "測試用看板" in board_names:
   button_to_click = A.find_ele_after_present(10,trello_page_locator['board_overflow_menu'])
   mouse.move_to_element(button_to_click).perform()
   button_to_click.click()
   button_to_click = A.find_ele_after_clickable(10,trello_page_locator['close_board'])
   button_to_click.click()
   button_to_click = A.find_ele_after_clickable(10,trello_page_locator['confirm_close_board'])
   button_to_click.click()
   button_to_click = A.find_ele_after_clickable(10,trello_page_locator['check_closed_board'])
   button_to_click.click()
   button_to_click = A.find_ele_after_clickable(10,trello_page_locator['delete_board'])
   button_to_click.click()
   button_to_click = A.find_ele_after_clickable(10,trello_page_locator['delete_board_confirm'])
   button_to_click.click()
   button_to_click = A.find_ele_after_clickable(10,trello_page_locator['leave_closed_board'])
   button_to_click.click()
   finish_test = True
else:
   print("測試用看板不存在。")    

if finish_test:
   board_list = A.find_ele_after_located(10,trello_page_locator['boards'])
   board_names = [board.text for board in board_list]
   if "測試用看板" not in board_names:
      print("測試通過！")
   else:
      print("測試失敗！")
else:
   print("未順利進行測試！")





