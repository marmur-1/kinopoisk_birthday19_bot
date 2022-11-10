import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.kinopoisk.ru/special/birthday19/?utm_source=kinopoisk&utm_medium=selfpromo_kinopoisk&utm_term=app_banner&utm_campaign=kinopoisk19_game&utm_content=plus"
with open("config.json", "r") as read_file:
    data = json.load(read_file)

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)

# --------------------------------------РЕГИСТРАЦИЯ-------------------------------------------#
# Вход в аккаунт
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.header__btn')))
element.click() 
# Ввод логина
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'passp-field-login')))
element.send_keys(data['login'])
# нажатие на кнопку ВОЙТИ
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'passp:sign-in')))
element.click() 
# Ввод пароля
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'passp-field-passwd')))
element.send_keys(data['password'])
# нажатие на кнопку ВОЙТИ
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'passp:sign-in')))
element.click() 


while True:
    print()