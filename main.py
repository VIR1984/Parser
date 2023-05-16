import json
import requests
from bs4 import BeautifulSoup
import lxml

#
# person_url_list = []
# for i in range(0, 746, 12):
#     url = f"https://www.bundestag.de/ajax/filterlist/de/abgeordnete/biografien/862712-862712?limit=12&noFilterSet=true&offset={i}"
#     # print(url)
#
#     q = requests.get(url)
#     result = q.content
#
#     soup = BeautifulSoup(result, 'lxml')
#     persons = soup.find_all('div', class_='bt-slide-content')
#
#     # print(persons)
#
#     for search in persons:
#         link = search.find('a')['href']
#         new_link = "https://www.bundestag.de" + link
#         person_url_list.append(new_link)
#
#
#
# with open('persons_url_list.txt', 'a') as file:
#     for line in person_url_list:
#         file.write(f'{line}\n')


with open('persons_url_list.txt') as file:
    lines = [line.strip() for line in file.readlines()]

    data_dict = []
    count = 0

    for line in lines:
        q = requests.get(line)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')
        person = soup.find(class_='bt-biografie-name').find('h3').text
        person_name_company = person.strip().split(',')
        person_name = person_name_company[0]
        person_company = person_name_company[1].strip()

        social_networks = soup.find_all(class_='bt-link-extern')

        social_network_urls = []
        if social_networks is not None:
            for item in social_networks:
                social_network_urls.append(item.get('href'))

        data = {
            'person_name': person_name,
            'company_name': person_company,
            'social_networks': social_network_urls

        }
        count += 1
        print(f'#{count}: {line} is done!')

        data_dict.append(data)

        print(data)

        with open('data.json', 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
