import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from _datetime import datetime
from dateparser import parse

def extract_news_by_date(target_date,max_pages):
    base_url = "https://kaztag.kz/ru/news"
    driver = webdriver.Chrome()
    news = []


    for page in range(1,max_pages+1):

        active_url = f"{base_url}?PAGEN_1={page}"
        print(page)
        print(active_url)
        driver.get(active_url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        news_elements = soup.find_all("div", class_="post type-post double")
        for news_element in news_elements:
            time.sleep(1)
            # Найдите дату публикации новости
            date_string = news_element.find("div", class_="post-byline").text.strip()
            #Форматирование даты
            news_date = parse(date_string)
            #Поиск URL новости
            links = news_element.find("a").get("href")
            news_link = "https://kaztag.kz" + links



            if news_date > target_date: #что то не так с датой постоянно выдает 22 сентября (Потому что не переходит на след стр) все понятно
                # Поиск контента
                #Тут приходится инициализировать новый запрос для полученного линка чтобы выйти на след стр МБ использовать новую функцию и подклбючать ее сюда
                driver.get(news_link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                news_desc_element = soup.find_all("div",class_="post-content")
                news_desc_p = soup.find_all("p") if news_desc_element else []
                news_desc_c = " ".join([p.get_text(strip=True)for p in news_desc_p])
                title = soup.find("h1", class_="post-title").get_text()



                result = {'title': title,
                  'news_desc_c': news_desc_c,
                  'date_string': date_string,
                  'news_link': news_link
                 }
                news.append(result)
    time.sleep(10)

    return news

target_date = datetime(2023, 9, 1, 12, 0)
start = extract_news_by_date(target_date,5)
print(start)