import requests
import fake_headers
from bs4 import BeautifulSoup
import re
import json

def find_vacancys():

    headers_gen = fake_headers.Headers(browser='firefox', os='win')
    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_gen.generate())
    html_data = response.text

    hh_main = BeautifulSoup(html_data, 'lxml')

    post_tag_list = hh_main.find('div', id='a11y-main-content')
    post_tags_all = post_tag_list.findAll('div', class_='vacancy-serp-item-body__main-info')

    vacancys_data = []
    for post in post_tags_all:

        name_tag = post.find('a', class_='serp-item__title')
        name = name_tag.text
        link = name_tag['href']

        salary_tag = post.find('span', class_='bloko-header-section-2')
        if salary_tag != None:
            salary = salary_tag.text
        else:
            salary = 'Не указано'

        company = post.find('a', class_='bloko-link bloko-link_kind-tertiary').text
        city = post.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text

        response_vac = requests.get(link, headers=headers_gen.generate())
        html_vac = response_vac.text
        hh_vac = BeautifulSoup(html_vac, 'lxml')
        vac_discription = hh_vac.find('div', class_='g-user-content')
        if vac_discription != None:
            vac_discription = vac_discription.text
            pattern = '(Django|django)|(Flask|flask)'
            res = re.findall(pattern, vac_discription)
            if res != None:
                vacancys_data.append({
                    'name': name,
                    'link': link,
                    'salary': salary,
                    'company': company,
                    'city': city
                })
    return vacancys_data

if __name__ == '__main__':
    vacancys_data = find_vacancys()
    with open('vacancy_data.json', 'w', encoding='utf-8', newline='') as f:
        json.dump(vacancys_data, f, ensure_ascii=False)