'''
Reference By :
Jinil Kim. 2022. Automated-Lecture-Assessment.
https://github.com/Global-Handong-Oriented-Security-Team/Automated-Lecture-Assessment. (2023).
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
from datetime import datetime
import os
import getpass


if __name__ == '__main__':
    hisnet_id = input("Enter a hisnet id: ")
    hisnet_pw = getpass.getpass("Enter a hisnet password: ")

    location = input("Enter the location for overnight leave : ")
    reason_text = input("Enter the reason for overnight leave : ")

    # Install and Generate Chrome driver
    chromedriver_path = os.getcwd() + "/chromedriver"
    driver = webdriver.Chrome(chromedriver_path)
    driver.implicitly_wait(3)

    # Open hisnet site
    driver.maximize_window()
    driver.get('https://hisnet.handong.edu/login/login.php')

    # Enter the ID and PW
    username = driver.find_element(By.NAME, 'id')
    username.send_keys(hisnet_id)

    username = driver.find_element(By.NAME, 'password')
    username.send_keys(hisnet_pw)

    # Clink login button
    driver.find_element(By.XPATH, "//input[@src='/2012_images/intro/btn_login.gif']").click()
    # Wait for some time to see the result
    driver.implicitly_wait(3)

    # Open RCpage
    driver.find_element(By.XPATH, "//div[contains(text(), '/RC')]").click()
    driver.implicitly_wait(3)

    # Switch to the new window
    main_window_handle = driver.window_handles[0]  # Store the handle of the main window
    new_window_handle = driver.window_handles[1]   # Store the handle of the new window
    driver.switch_to.window(new_window_handle)     # Switch to the new window

    # Open mypage
    driver.get('https://rc.handong.edu/rc/mypage/index.do?menu_idx=152')
    driver.implicitly_wait(3)

    # Open Apply sleepover page
    driver.get('https://rc.handong.edu/rc/mypage/domExeat/index.do?menu_idx=70')
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
    
    
    while day <= end_day_of_month :
        formated_time =  f'{year}-{formated_month}-{day}'

        # Remove "readonly" attribute from the date input
        driver.execute_script("document.getElementById('ovng_begin_dttm').removeAttribute('readonly');")

        # Find the date input element and send today's date
        date_input = driver.find_element(By.ID, 'ovng_begin_dttm')
        date_input.clear()  # Clear any existing value
        date_input.send_keys(formated_time)

        # Write reason
        reason = driver.find_element(By.NAME, 'ovng_resn')
        reason.clear()
        text = location + "\n" + reason_text
        reason.send_keys(text)

        day = day + 1

        time.sleep(3)

        # Click apply button
        driver.find_element(By.XPATH, "//button[@class='btn bg_purple'][text()='신청하기(Apply)']").click()

        # Wait for the confirmation message box to appear
        # driver.implicitly_wait(2)  # Need to adjust the wait time based on page loading speed
        time.sleep(1)
        
        # Switch to the alert and accept it
        alert = driver.switch_to.alert
        alert.accept()
        
        # Wait for some time to see the result
        driver.implicitly_wait(5)
    
    driver.quit()

        

        









    
    





