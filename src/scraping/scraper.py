import requests
from bs4 import BeautifulSoup as bs
import codecs

__all__ = ('rabota_by', 'belmeta')


headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.example'  # This is another valid field
}


def rabota_by(url):
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = bs(resp.text, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
        jobs = []
        for div in divs:
            url = div.find('a', attrs={'class': 'serp-item__title'})['href']
            title = div.find('a', attrs={'class': 'serp-item__title'}).text
            description = (div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})).text
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            if url and title and description and company:
                jobs.append({'title': title, 'url': url, 'description': description, 'company': company})

    return jobs


def belmeta(url):
    domain = 'https://belmeta.com/'
    jobs = []
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = bs(resp.text, 'html.parser')
        arts = soup.find_all('article', attrs={'class': 'job no-logo'})
        for art in arts:
            url = domain + art.a['href']
            title = art.a.text
            description = art.find('div', attrs={'class': 'desc'}).text
            company = art.find('div', attrs={'class': 'job-data company'}).text

            if url and title and description and company:
                jobs.append({'title': title, 'url': url, 'description': description.replace('\r\n      ', '').replace('\r\n    ', ''), 'company': company})

    return jobs

belmeta('https://belmeta.com/vacansii?q=python&l=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA')
