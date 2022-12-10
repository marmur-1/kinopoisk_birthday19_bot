from random import randrange
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint

url = "https://www.kinopoisk.ru/special/birthday19/?utm_source=kinopoisk&utm_medium=selfpromo_kinopoisk&utm_term=app_banner&utm_campaign=kinopoisk19_game&utm_content=plus"
with open("config.json", "r") as read_file:
    data = json.load(read_file)
with open("answer_ep5.json", "r",encoding='utf8') as read_file:
    answer_data = json.load(read_file)

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)

# --------------------------------------РЕГИСТРАЦИЯ-------------------------------------------#
# Вход в аккаунт
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.header__button')))
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

# ----------------------------------------СТАРТ ИГРЫ---------------------------------------------#
# нажатие на кнопку ИГРАТЬ
time.sleep(5)
element = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.episode-card__btn')))[4]
element.click() 
# Выбор вселенной
time.sleep(5)
univers = randint(0, 9)
print("Вселенная номер: "+str(univers))
element = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.modal-multigame__game-card')))
element[univers].click() 

# ------------------------------------------ИГРА------------------------------------------------#
while True:
    while True:
        # цитата
        time.sleep(randrange(5, 20))
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.game__test-question')))
        question = element.text
        # print(img_url)
        # кнопки с ответами
        answer_btns = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.game__test-answers-item')))
        # ответ из файла
        answer = None
        try:
            answer = answer_data[str(univers)][question]
            print("Ответ "+answer)
        except KeyError:
            print("Нет ответа")
        # выбр ответа
        trust_answer = None
        try:
            a = 0
            for btn in answer_btns:     
                btn_text = WebDriverWait(btn, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.text-fit'))).text
                if answer==None: #Ести готового ответа нет
                    btn.click()
                    time.sleep(0.5)
                    b = btn.get_attribute('class')
                    if b == "game__test-answers-item game__test-answers-item_state_error":
                        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.modal-wrong-answer__title')))
                        text = element.text
                        text = text.split("«")[1]
                        text = text.split("»")[0]
                        answer_data[str(univers)][question] = text
                        print('Ошибка')
                        trust_answer = False
                    else:
                        print('Верно')
                        answer_data[str(univers)][question] = btn_text
                        trust_answer = True
                    break
                else: #Ести готового ответ есть
                    if btn_text == answer:
                        btn.click()
                        trust_answer = True
                        break
                a = a+1
            # Исправление неверных ответов в файле
            if a >=4:
                btn_text = WebDriverWait(answer_btns[0], 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.text-fit'))).text
                answer_btns[0].click()
                b = answer_btns[0].get_attribute('class')
                if b == "game__test-answers-item game__test-answers-item_state_error":
                    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.modal-wrong-answer__title')))
                    text = element.text
                    text = text.split("«")[1]
                    text = text.split("»")[0]
                    answer_data[str(univers)][question] = text
                    print('Ошибка')
                    trust_answer = False
                else:
                    print('Верно')
                    answer_data[str(univers)][question] = btn_text
                    trust_answer = True
                break
            # Запись правильного ответа в файл
            with open('answer_ep5.json',"w",encoding='utf8') as file:
                json.dump(answer_data,file,ensure_ascii=False)
        except Exception:
            print("Ошибка при выборе ответа")

        # Следующая игра
        try:
            next_btns_div = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.modal-wrong-answer__content')))
            next_btns = answer_btns = WebDriverWait(next_btns_div, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.button')))
            if trust_answer == True:
                print("Удаление ошибки")
                answer_data[str(univers)].pop(question)
            for next_btn in next_btns:
                if next_btn.text == "Продолжить игру":
                    next_btn.click()
                    break
                elif next_btn.text == "Играть ещё раз":
                    time.sleep(5)
                    next_btn.click()
                    break
        except Exception:
            if trust_answer == False:
                print("Удаление ошибки")
                answer_data[str(univers)].pop(question)
        finally:
            print("Следующий вопрос")
            
