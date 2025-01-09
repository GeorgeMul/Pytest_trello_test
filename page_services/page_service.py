from page_object.page_object import Operator

class Service():
    def __init__(self,driver):
        self.operator = Operator(driver)

    def login(self,URL,email,pwd):
        self.operator.driver.get(URL)
        self.operator.send_keys_to_element('input_email',email)
        self.operator.click_button('login_submit')
        self.operator.send_keys_to_element('input_password',pwd)
        self.operator.click_button('login_submit')
    
    def into_workspace(self):
        self.operator.click_button('workspace_switcher')
        self.operator.click_button('into_workspace')
    
    def create_board(self,board_title):
        self.operator.click_button('create_board_button')
        self.operator.send_keys_to_element('input_board_title',board_title)
        self.operator.click_button('create_board_submit')

    def delete_board(self):
        self.operator.click_button('board_overflow_menu')
        self.operator.click_button('close_board')
        self.operator.click_button('confirm_close_board')
        self.operator.click_button('check_closed_board')
        self.operator.click_button('delete_board')
        self.operator.click_button('delete_board_confirm')
        self.operator.click_button('leave_closed_board')

    def create_list(self,list_title):
        self.operator.click_button('create_board_button')
        self.operator.send_keys_to_element('new_listname_input',list_title)
        self.operator.click_button('create_list_submit')

    def delete_list(self):
        self.operator.click_button('list_overflow_menu')
        self.operator.click_button('archive_list_button')
        self.operator.click_button('overflow_menu_inboard')
        self.operator.click_button('check_archived')
        self.operator.click_button('archived-switcher')
        self.operator.click_button('delete_list')
        self.operator.click_button('delete_confirm')
    
    def create_card(self,card_title):
        self.operator.click_button('create_card_button')
        self.operator.send_keys_to_element('new_cardname_input',card_title)
        self.operator.click_button('create_card_submit')

    def delete_card(self):
        self.operator.click_button('card-button')
        self.operator.click_button('card-archive-button')
        self.operator.click_button('card-delete-button')

    def add_description_to_card(self,text_context):
        self.operator.click_button('card-button')
        self.operator.click_button('add_description_button')
        self.operator.send_keys_to_element('card_description_textarea',text_context)
        self.operator.click_button('description_save_button')






