from logging import error
from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from datetime import time, datetime, timezone, timedelta
from typing import Tuple
from time import sleep

# login info
mail = "abcxyz@gmail.com"
password = "abc123"

# time to start program
begin_time = time(12,00)
end_time = time(13,00)
max_try = 100000

vn_time = timezone(timedelta(hours=+7), 'VN_TIME')

# initialize the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option('debuggerAddress', 'localhost:9014')
driver = webdriver.Chrome(options=options)

# to check current time
def check_current_time(begin_time:time, end_time:time) -> Tuple[time, bool]:
    dt_now = datetime.now(vn_time)
    current_time = time(dt_now.hour, dt_now.minute, dt_now.second)
    return current_time, (begin_time <= current_time) and (current_time < end_time)

# to login
def login():
    # go to login page
    driver.get("https://ticketbox.vn/sign-in?ref=/")
    try:
        element = WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.XPATH, '//button[text()="Tiếp tục"]' or '//button[text()="Continue"]'))
            EC.presence_of_element_located((By.CSS_SELECTOR, '[alt="login email"]'))
        )
    finally:
        # head to login using gmail
        driver.find_element(By.CSS_SELECTOR, '[alt="login email"]').click()
    # find username/email field and send the username itself to the input field
    driver.find_element("name", "email").send_keys(mail)
    # find password input field and insert password as well
    driver.find_element("name", "password").send_keys(password)
    # click login button
    driver.find_element(By.XPATH, '//button[text()="Tiếp tục" or text()="Continue"]').click()
    sleep(3)

# to go to buy ticket button
def buy_ticket_button():
    driver.get("https://ticketbox.vn/event/born-pink-world-tour-hanoi-2023-87722")
    # BUY TICKET button
    try:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Bg_bg__8PaBD"))
            )
        finally:
            element = driver.find_element(By.XPATH, '//*[contains(text(),"*Theo giờ Việt Nam")]')
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
        return True
    except Exception as e:
        print(e)
        return False

# to buy ticket
def ticket_page():
    # initialize the params
    current_time, is_during_running_time = check_current_time(begin_time, end_time)
    reservation_completed = False
    try_num = 1

    # retry every second
    while True:
        if not is_during_running_time:
            print(f'Not Running the program. It is {current_time} and not between {begin_time} and {end_time}')

            # sleep less as the time gets closer to the begin_time
            if current_time >= time(11,59,59):
                sleep(0.001)
            elif time(11,59,58) <= current_time < time(11,59,59):
                sleep(0.5)
            else:
                sleep(1)

            try_num += 1
            current_time, is_during_running_time = check_current_time(begin_time, end_time)
            continue

        print(f'----- try : {try_num} -----')
        # get to buy button
        reservation_completed = buy_ticket_button()

        if reservation_completed:
            print('GO TIME!')
            break
        elif try_num == max_try:
            print(f'Tried {try_num} times, but couldn\'t access..')
            break
        else:
            sleep(1)
            try_num += 1
            current_time, is_during_running_time = check_current_time(begin_time, end_time)


if __name__ == "__main__":
    # login()
    ticket_page()
    while(True):
        pass
