import asyncio
import codecs
import os.path
import sys
# from time import time
from django.contrib.auth import get_user_model
from django.db import DatabaseError

from scraping.scraper import *

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()
from scraping.models import City, Vacancy, Language, Url

User = get_user_model()
jobs = []
parsers = ((rabota_by, 'rabota'),
           (belmeta, 'belmeta'))


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {'city': pair[0], 'language': pair[1], 'url_data': url_dict[pair]}
        urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job = await loop.run_in_executor(None, func, url, city, language)
    jobs.extend(job)


# start = time()
settings = get_settings()
url_list = get_urls(settings)
loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
#
# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j = func(url, city=data['city'], language=data['language'])
#         jobs += j

loop.run_until_complete(tasks)
loop.close()
# end = time() - start
for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

h = codecs.open('works.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()