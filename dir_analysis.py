import os
import csv
from datetime import datetime

path = r'F:\Others'

# Получение списка всех файлов в директории и ее поддиректориях
files = []
for root, directories, file_names in os.walk(path):
    for filename in file_names:
        files.append(os.path.join(root, filename))

# Сбор информации о каждом файле
file_info = []
for file_path in files:
    statinfo = os.stat(file_path)
    size_gb = round(statinfo.st_size / (1024**3), 3)
    last_modified = datetime.fromtimestamp(statinfo.st_mtime).strftime('%d.%m.%Y')
    file_info.append({
        'FullName': file_path,
        'Name': os.path.basename(file_path),
        'SizeGB': size_gb,
        'LastWriteTime': last_modified
    })

# Сортировка результатов по размеру файла по убыванию и вывод 1000 первых записей
sorted_file_info = sorted(file_info, key=lambda x: x['SizeGB'], reverse=True)[:1000]

# Запись результатов в CSV-файл с кодировкой Windows-1251
with open(r'F:\Others\output2.csv', 'w', encoding='windows-1251', newline='') as csvfile:
    fieldnames = ['FullName', 'Name', 'SizeGB', 'LastWriteTime']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    for row in sorted_file_info:
        writer.writerow(row)
