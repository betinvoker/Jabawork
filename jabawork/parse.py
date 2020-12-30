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
    #   Проверить и заполнить таблицу Universities.
    changing_the_table_universities()
    #   Проверить и заполнить таблици Opinions. 
    filling_in_the_table_opinions()
    #   Закрыть браузер после выполнения
    driver.close()

#   Проверить таблицу Universities на заполненность.
#   Если в ней уже есть записи, то сравнить последнюю запись с первой записью на странице.
#   Иначе, просто заполнить таблицу. 
def changing_the_table_universities():
    #   Главная страница сайта
    driver.get("https://tabiturient.ru/")
    #   Нажимать на кнопку загрузить еще, пока она существует на странице
    click_btn_universities()
    block = driver.find_element_by_id('resultdiv0')
    all_universities = len(block.find_elements_by_class_name('mobpadd20'))
    #   Берем количество записей из таблицы Universities и присваиваем его переменной
    sqlite_select_count_universities = "SELECT COUNT(*) FROM search_reviews_universities"
    cursor.execute(sqlite_select_count_universities)
    count_universities = int(cursor.fetchone()[0])
    #   Если количество записей в таблице больше нуля, то выполняем условие.
    #   Если оно равно нулю, тогда заполняем таблицу данными со страницы сайта.
    if count_universities == all_universities:
        #   Пока не придумал, что должно тут выводиться
        print("Таблица Universities содержит - " + str(count_universities) + " записей из "+ str(all_universities) +"\n")
    else:
        print("Таблица Universities содержит - " + str(count_universities) + " записей из "+ str(all_universities) +"\n")
        #   Парсить данные об университетах со страницы
        parse_list_of_universities()

#   Заполнение таблици Opinions.
def filling_in_the_table_opinions():
    #   Взять из базы список университетов
    sqlite_select_query = "SELECT * from search_reviews_universities"
    cursor.execute(sqlite_select_query)
    all_universities = cursor.fetchall()
    #   Перебрать все университеты по списку
    for university in all_universities:
        #   Берем количество записей из таблицы Opinions и присваиваем его переменной
        sqlite_select_count_opinions = "SELECT search_reviews_universities.id, COUNT(search_reviews_opinions.university_id) FROM search_reviews_universities LEFT JOIN search_reviews_opinions ON search_reviews_universities.id = search_reviews_opinions.university_id WHERE search_reviews_universities.id = "  + str(university[0]) + " GROUP BY search_reviews_universities.id"
        cursor.execute(sqlite_select_count_opinions)
        count_opinions = int(cursor.fetchone()[1])

        driver.get(university[3])
        click_btn_opinions()
        time.sleep(5)
        all_opinions = int(len(list(driver.find_elements_by_class_name('mobpadd20-2'))))
        #   Если количество записей в таблице больше нуля, то выполняем условие.
        #   Если оно равно нулю, тогда заполняем таблицу данными со страницы сайта.
        print(str(university[1]) + " | Кол-во отзывов - " + str(count_opinions) + "/" + str(all_opinions) + "\n")
        if count_opinions > all_opinions:
            print(str(university[1]) + " | Кол-во отзывов - " + str(count_opinions) + "/" + str(all_opinions) + "\n")
            parse_list_of_opinions(university[0])
        else:
            parse_list_of_opinions(university[0])

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
def click_btn_opinions():
    while check_exists_by_class_name('mobpadd10') == True:
        btn = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[7]')
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
        adding_universities(abbreviation.text, full_name.text, link.get_attribute("href"), logo.get_attribute("src")[31:], link_universitiy)
        
        i += 1
    #   Сохранить изменения в базе
    conn.commit()

#   Парсить данные с отзывами об университете
def parse_list_of_opinions(university):
    block = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]')
    all_opinions = reversed(block.find_elements_by_class_name('mobpadd20-2'))

    i = 1
    #   Цикл сбора данных и записи данных об университете
    for opinion in all_opinions:
        #   Нажимать на ссылку "Показать полностью..."
        click_on_show_link(opinion, '/html/body/div[1]/div[2]/div[1]/div/div[5]/div[' + str(i) + ']/div[1]/div[2]/b')

        text = opinion.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]/div[' + str(i) + ']/div[1]/div[2]')
        date_opinion = opinion.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[5]/div[1]/div[1]/div[1]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[5]/span[2]')
        picture = opinion.find_element_by_tag_name("img")

        id_university = str(university)
        if picture.get_attribute("src") == "https://tabiturient.ru/img/smile2.png":
            opinion = "False"
        else:
            opinion = "True"
        
        
        
        print(text.text + " | " + date_opinion.text + " | " + opinion + " | " + id_university + "\n")
        adding_opinions(text.text, date_opinion.text, opinion, id_university)
        
        i += 1

    #   Сохранить изменения в базе
    conn.commit()

#   Добавить университет в базу
def adding_universities(abbreviated, full_name, link, logo, link_universitiy):
    cursor.execute("INSERT INTO search_reviews_universities(abbreviated, name, link, logo, link_universitiy) VALUES (?,?,?,?,?)", 
                        (abbreviated, full_name, link, logo, link_universitiy))
       
#   Добавить отзывов об университете в базу
def adding_opinions(text, date_opinion, opinion, id_university):
    cursor.execute("INSERT INTO search_reviews_opinions(text, date_opinion, opinion, university_id) VALUES (?,?,?,?)", 
                        (text, date_opinion, opinion, id_university))

#   Нажимать на ссылку "Показать полностью..."
def click_on_show_link(opinion, show_full):
    if check_exists_by_xpath(show_full):
        btn = opinion.find_element_by_xpath(show_full)
        driver.execute_script("arguments[0].click();", btn)

#   Проверка элемента на наличие по классу
def check_exists_by_class_name(class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

#   Проверка элемента на наличие по xpath
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

if __name__ == "__main__":
    main()
