import requests
from bs4 import BeautifulSoup
import pandas as pd

# Базовый URL-адрес веб-сайта
base_url = "https://www.greeninfo.ru/alphabet.html/letter/"

# Количество страниц
num_pages = 28

# Создаем список для хранения данных
l = []

# Проходим по каждой странице
for page_num in range(num_pages):
    # Создаем полный URL-адрес для каждой страницы
    url = base_url + str(page_num)
    
    # Отправляем GET-запрос по URL-адресу
    response = requests.get(url)
    
    # Анализируем HTML-содержимое
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Находим все элементы с классом "em14"
    names = soup.find_all(class_="em14")
    
    # Извлекаем названия продуктов и записываем их в созданный список
    for element in names:
        name = element.text.strip()
        l.append(name)
    
    # Отслеживаем выполнение
    print("Страница", page_num, "просмотрена.")

print("Извлечение данных завершено. Сохранено в переменной l")

# Конвертируем список в датафрейм и экспортируем в csv
df = pd.DataFrame(l, columns=['name'])
df.to_csv('botanic_dictionary.csv', index=False, sep='\t', encoding='utf-16')
