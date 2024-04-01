'''
Reference By :
Jinil Kim. 2022. Automated-Lecture-Assessment.
https://github.com/Global-Handong-Oriented-Security-Team/Automated-Lecture-Assessment. (2023).
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

import time
from datetime import datetime
import os
import getpass


def clickSpecificDate(driver, date):
    date_element = driver.find_element(By.ID, date)
    date_element.click()
    
    
def clickDropdownOption(driver, dropdown_id, option_value):
    dropdown = Select(driver.find_element(By.ID, dropdown_id))
    dropdown.select_by_value(option_value)
    


if __name__ == '__main__':
    
    student_num = input("Enter a student number: ")
    hisnet_id = input("Enter a hisnet id: ")
    hisnet_pw = getpass.getpass("Enter a hisnet password: ")
    location = input("Enter the location for overnight leave : ")
    reason_text = input("Enter the reason for overnight leave : ")

     # Install and Generate Chrome driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    

    # Open hisnet site
    driver.maximize_window() 
    driver.get('https://hisnet.handong.edu/login/login.php')

    # Enter the ID and PW
    username = driver.find_element(By.NAME, 'id_1')
    username.send_keys(hisnet_id)

    username = driver.find_element(By.NAME, 'password_1')
    username.send_keys(hisnet_pw)

    # Clink login button
    driver.find_element(By.XPATH, "//input[@src='/2012_images/intro/btn_login.gif']").click()
    # Wait for some time to see the result
    driver.implicitly_wait(3)

    # Switch to the new window
    main_window_handle = driver.window_handles[0]  # Store the handle of the main window
    new_window_handle = driver.window_handles[1]   # Store the handle of the new window
    driver.switch_to.window(new_window_handle)     # Switch to the new window

    # Open RCpage
    driver.get('https:\/\/rc.handong.edu/')
    driver.implicitly_wait(3)

    # Open Apply login page of RC
    driver.get('https://rc.handong.edu/90/9040.do')
    driver.implicitly_wait(3)
    
    # Enter the student ID and PW
    userid = driver.find_element(By.NAME, 'id')
    userid.send_keys(student_num)

    rcpassword = driver.find_element(By.NAME, 'pw')
    rcpassword.send_keys(hisnet_pw)
    
    # Clink login button
    login_button = driver.find_element(By.CLASS_NAME, "btn_login")
    login_button.click()
    
    # Open Apply sleepover page
    driver.get('https://rc.handong.edu/70/7030.do')
    driver.implicitly_wait(3)  
    
    # Intiate the formated_date, year, month and day
    now = datetime.now()
    year = now.year
    month = now.month
    formated_month = f"{now.month:02d}"
    day = now.day

    # Set end_day_of_month
    import calendar
    end_day_of_month = calendar.monthrange(year, month)[1]
    
    
    while (day+5) <= end_day_of_month :
        
        stayout_button = driver.find_element(By.XPATH, "//a[@class='btn b_Blu right_p1 wd80' and contains(text(), '외박신청')]")
        stayout_button.click()
        stayout_button.click()
        
        # Click on dates for 6 times
        for i in range(6):
            formated_time =  f'{year}-{formated_month}-{day:02d}'
            clickSpecificDate(driver, formated_time)
            time.sleep(1);
            day = day + 1
        
        # Click reason list
        dropdown_id = "sleepsayou"  # 예제 목록 id, 실제 목록 id로 수정해야 합니다.
        option_value_to_select = "99"  # 선택할 옵션의 값, 실제 목록에 따라 수정해야 합니다.

        clickDropdownOption(driver, dropdown_id, option_value_to_select)
        time.sleep(1)
        
        # Write location and reason
        # Find the sl_content element
        sl_content_element = driver.find_element(By.ID, 'sl_content')
        # Input location and reason_text into sl_content
        sl_content_element.send_keys(f"장소: {location}, 사유: {reason_text}")
        time.sleep(2)
        
        # Click apply button
        apply_button = driver.find_element(By.XPATH, "//a[@class='btn b_Blu center_p1 wd110' and contains(text(), '(Apply)')]")
        apply_button.click()
        
        # Wait for the confirmation message box to appear
        driver.implicitly_wait(2)  # Need to adjust the wait time based on page loading speed
        
        # Switch to the alert and accept it
        alert = driver.switch_to.alert
        alert.accept()
        
        # Wait for some time to see the result
        driver.implicitly_wait(5)
        
        
    # Click the dates of rest until end_day_of_month
    if day < end_day_of_month:
        stayout_button = driver.find_element(By.XPATH, "//a[@class='btn b_Blu right_p1 wd80' and contains(text(), '외박신청')]")
        stayout_button.click()
    
        while day <= end_day_of_month:
            formated_time =  f'{year}-{formated_month}-{day:02d}'
            clickSpecificDate(driver, formated_time)
            time.sleep(1);
            day = day + 1
        
        # Click reason list
        dropdown_id = "sleepsayou"  # 예제 목록 id, 실제 목록 id로 수정해야 합니다.
        option_value_to_select = "99"  # 선택할 옵션의 값, 실제 목록에 따라 수정해야 합니다.

        clickDropdownOption(driver, dropdown_id, option_value_to_select)
        time.sleep(1)
        
        # Write location and reason
        # Find the sl_content element
        sl_content_element = driver.find_element(By.ID, 'sl_content')
        # Input location and reason_text into sl_content
        sl_content_element.send_keys(f"장소: {location}, 사유: {reason_text}")
        time.sleep(1)
        
        # cancel_btn = driver.find_element(By.CLASS_NAME, "cancel_btn")
        # cancel_btn.click()
        # time.sleep(1)

        # Click apply button
        apply_button = driver.find_element(By.XPATH, "//a[@class='btn b_Blu center_p1 wd110' and contains(text(), '(Apply)')]")
        apply_button.click()
        
        # Wait for the confirmation message box to appear
        driver.implicitly_wait(2)  # Need to adjust the wait time based on page loading speed
        
        # Switch to the alert and accept it
        alert = driver.switch_to.alert
        alert.accept()
        
        # Wait for some time to see the result
        driver.implicitly_wait(5)
    
    driver.quit()

        

        









    
    





