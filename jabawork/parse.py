from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sqlite3
import os
import time

path = r"chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)

conn = sqlite3.connect('db.sqlite3')
#   Создать соединение с базой
cursor = conn.cursor()

def main():
    #   Главная страница сайта
    #driver.get("https://tabiturient.ru/")
    #   Нажимать на кнопку загрузить еще, пока она существует на странице
    #click_btn_universities()
    #   Парсить данные об университетах со страницы
    #parse_list_of_universities()
    #   Закрыть браузер после выполнения
    #driver.close()

    sqlite_select_query = "SELECT * from search_reviews_universities"
    cursor.execute(sqlite_select_query)
    all_universities = cursor.fetchall()

    for university in all_universities:
    #   Страница с отзывами об университете
        click_btn_reviews(university[3])
        parse_list_of_reviews(university[0])


#   Нажимать на кнопку загрузить еще, пока она существует на странице
def click_btn_universities():
    btn = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]')
    while True:
        if driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]').is_displayed():
            btn.click()
            time.sleep(5)
        else:
            break

#   Открыть страницу с отзывами и нажимать кнопку, пока она существует на странице
def click_btn_reviews(link):
    driver.get(link)

    btn = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[7]')

    while driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[7]') == True:
        if btn.is_displayed():
            btn.click()
            time.sleep(5)
        else:
            break

#   Парсить данные об университетах со страницы
def parse_list_of_universities():  
    block = driver.find_element_by_id('resultdiv0')
    all_universities = block.find_elements_by_class_name('mobpadd20')

    i = 1

    #   Цикл сбора данных и записи данных об университете
    for university in all_universities:
        abbreviation = university.find_element_by_class_name('font3')
        full_name = university.find_element_by_class_name('font2')
        link = university.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]/div[' + str(i) + ']/table[2]/tbody/tr[2]/td/a[3]')
        logo = university.find_element_by_class_name('vuzlistimg')
        link_universitiy = logo.get_attribute("src")[31:-4]

        print(abbreviation.text + " | " + full_name.text + " | " + link.get_attribute("href") + " | " + logo.get_attribute("src")[31:] + " | " + link_universitiy + "\n")
        #   Добавить университет в базу
        #adding_universities(abbreviation.text, full_name.text, link.get_attribute("href"), logo.get_attribute("src")[31:], link_universitiy)
        
        i += 1
    #   Сохранить изменения в базе
    conn.commit()

def parse_list_of_reviews(university):  
    block = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]')
    all_reviews = block.find_elements_by_class_name('mobpadd20-2')

    i = 1

    #   Цикл сбора данных и записи данных об университете
    for review in all_reviews:
        text = review.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]/div[' + str(i) + ']/div[1]/div[2]')
        date = review.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]/div[1]/div[1]/div[1]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[5]/span[2]')
        
        picture = review.find_element_by_tag_name("img")
        if picture.get_attribute("src") == "https://tabiturient.ru/img/smile2.png":
            opinion = "False"
        else:
            opinion = "True"
        
        id_university = str(university)

        print(text.text + " | " + date.text + " | " + opinion + " | " + id_university + "\n")
        adding_reviews(text.text, date.text, opinion, id_university)
        
        i += 1

    #   Сохранить изменения в базе
    conn.commit()

#   Добавить университет в базу
def adding_universities(abbreviated, date, link, logo, link_universitiy):
    cursor.execute("INSERT INTO search_reviews_universities(abbreviated, name, link, logo, link_universitiy) VALUES ('" 
                        + abbreviated + "','" + name + "','" + link + "','" + logo + "','" + link_universitiy + "')")
       
#   Добавить отзывов об университете в базу
def adding_reviews(text, date, opinion, id_university):
    cursor.execute("INSERT INTO search_reviews_opinions(text, date, opinion, university_id) VALUES ('" 
                        + text + "','" + date + "','" + opinion + "','" + id_university + "')")

if __name__ == "__main__":
    main()
