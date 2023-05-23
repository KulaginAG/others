import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.greeninfo.ru/alphabet.html/letter/"
num_pages = 28


def extract_names_from_page(page_num):
    url = base_url + str(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    names = soup.find_all(class_="em14")
    return [name.text.strip().lower() for name in names if len(name.text.strip()) < 50]


wordlist = []
for page_num in range(num_pages):
    wordlist += extract_names_from_page(page_num)
    print(f"Страница {page_num} просмотрена")

print("Извлечение данных завершено. Сохранено в переменной l")

df = pd.DataFrame(wordlist, columns=['name'])
df.to_csv('botanic_dictionary.csv', index=False, sep='\t')
