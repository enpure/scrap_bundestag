import requests
from bs4 import BeautifulSoup
import json

# # Настройки для имитации действий браузера
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#
# persons_url_list = []
#
# for i in range(0, 760, 20):
#     url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'
#     print(f"Processing: {url}")
#     q = requests.get(url, headers=headers)
#     result = q.content
#
#     soup = BeautifulSoup(result, 'lxml')
#     # Извлечение всех ссылок <a> с атрибутом 'href'
#     links = soup.find_all('a', href=True)
#
#     for link in links:
#         person_page_url = link['href']
#         # Проверяем, что URL абсолютный и соответствует ожидаемому паттерну
#         if person_page_url.startswith("https://www.bundestag.de/en/members/"):
#             persons_url_list.append(person_page_url)
#         else:
#             print(f"Ignored URL: {person_page_url}")
#
# # Запись результатов в файл
# with open('persons_url_list.txt', 'w') as file:
#     for line in persons_url_list:
#         file.write(f'{line}\n')
#
# print(f"Total unique URLs found: {len(set(persons_url_list))}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# предполагается, что у вас уже есть файл persons_url_list.txt со всеми ссылками

with open('persons_url_list.txt') as file:
    lines = [line.strip() for line in file.readlines()]

data_dict = []
count = 0
for line in lines:
    q = requests.get(line, headers=headers)
    result = q.content

    soup = BeautifulSoup(result, 'lxml')
    person_info = soup.find(class_='bt-biografie-name').find('h3')
    if person_info:
        person = person_info.text
        person_name_company = person.strip().split(',')
        person_name = person_name_company[0]
        company_name = person_name_company[1].strip() if len(person_name_company) > 1 else None

        social_networks = soup.find_all(class_='bt-linkliste')
        social_networks_url = []
        for item in social_networks:
            links = item.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                if href and (href.startswith('http://') or href.startswith('https://')):
                    social_networks_url.append(href)

        data = {
            'person_name': person_name,
            'company_name': company_name,
            'social_networks': social_networks_url
        }
        count += 1
        print(f"Processing: {count}: {line} is done!")
        data_dict.append(data)
    else:
        print(f"Person info not found for URL: {line}")

with open('data.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print(f"Total persons processed: {count}")