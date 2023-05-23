import time
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tqdm import tqdm
import pymorphy2
import nltk
from nltk.corpus import stopwords


def main():
    # Подготавливаем пакеты для обработки слов
    nltk.download('stopwords')
    morph = pymorphy2.MorphAnalyzer()
    stop_words = stopwords.words('russian')
    stop_words.extend(['см', 'м', 'г', 'кг', 'л', 'мл', ])
    # Применяем лемматизацию к названиям товаров
    df = pd.read_csv('preprocessing_data.csv')
    df['product_lem'] = df['product'].apply(
        lambda x: ' '.join([morph.parse(word)[0].normal_form for word in x.split() if word not in stop_words]))
    df = df['product_lem'].replace(to_replace=r'[a-zA-Z\W\d]+', value=' ', regex=True)
    df = df.drop_duplicates()

    # Подготавливаем датафреймы для работы парсера
    def read_files(df):
        try:
            product_category = pd.read_csv('data_categories.csv')
        except:
            product_category = pd.DataFrame({'name': [float('nan')],
                                             'level_1': [float('nan')],
                                             'level_2': [float('nan')],
                                             'level_3': [float('nan')],
                                             'level_4': [float('nan')]
                                             }
                                            )
        # Проверяем заполненные записи, чтобы избежать повторной обработки при перезапуске веб-драйвера
        df = df[~df.isin(product_category['name'])]
        return product_category, df

    product_category, df = read_files(df)

    # Приведение данных к нормальному виду и экспорт
    def update(product_category_upd, product_category):
        product_category_upd.reset_index(inplace=True)
        product_category_upd = product_category_upd.reindex(columns=['index', 0, 1, 2, 3])
        product_category_upd.columns = ['name', 'level_1', 'level_2', 'level_3', 'level_4']
        product_category = pd.concat([product_category, product_category_upd], ignore_index=True)
        product_category.dropna(how='all', inplace=True)
        product_category.to_csv('data_categories.csv', index=False)

    '''
    Выполняем парсинг до тех пор, пока не достигнем последнего элемента выборки.
    Веб-драйвер работает до тех пор, пока не появилась проверка с вводом слов по изображению (в таком случае идет 
    перезапуск веб-драйвера с сохранением датафрейма и продолжением с текущего места).
    '''
    while product_category['name'].iat[-1] != df.iat[-1]:
        goods = {}
        my_dict = df.unique().tolist()
        # Load the webpage
        url = 'https://market.yandex.ru'

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 2)
        driver.get(url)
        try:
            wait.until(ec.element_to_be_clickable((By.ID, "js-button")))
            driver.find_element(By.ID, "js-button").click()
            time.sleep(5)
        except:
            pass

        try:
            for k, i in zip(my_dict, tqdm(range(len(my_dict)), desc='Прогресс', position=0, leave=True)):
                # Ввод товара в поисковой строке
                driver.find_element(By.ID, "header-search").send_keys(k)
                driver.find_element(By.CSS_SELECTOR, "button[data-auto='search-button']").click()

                try:
                    driver.find_element(By.ID, "js-button").click()
                    time.sleep(random.randint(1, 3))
                except:
                    pass

                time.sleep(random.randint(1, 3))
                # Extract the HTML content
                html = driver.page_source

                # Запись данных HTML
                soup = BeautifulSoup(html, 'html.parser')
                # Поиск всех категорий и подкатегорий для товара
                category_elements = soup.find_all(itemprop='name')
                categories = []
                for category_element in category_elements[0:3]:
                    category_name = category_element.text
                    categories.append(category_name)

                goods.update({k: categories})

                driver.find_element(By.ID, "header-search").clear()

            # Запись товара и его категорий в датафрейм
            product_category_upd = pd.DataFrame.from_dict(goods, orient='index')
            # Остановка веб-драйвера (закрытие браузера)
            driver.quit()
            update(product_category_upd, product_category)


        except:
            # Запись товара и его категорий в датафрейм
            product_category_upd = pd.DataFrame.from_dict(goods, orient='index')
            # # Остановка веб-драйвера (закрытие браузера)
            driver.quit()

            update(product_category_upd, product_category)
            product_category, df = read_files(df)


if __name__ == '__main__':
    main()
