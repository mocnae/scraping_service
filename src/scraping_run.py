import codecs
import os.path
import sys

from django.db import DatabaseError

from scraping.scraper import *

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()
from scraping.models import City, Vacancy, Language
city = City.objects.filter(slug='minsk').first()
language = Language.objects.filter(slug='python').first()

parsers = ((rabota_by, 'https://rabota.by/search/vacancy?text=python&from=suggest_post&area=1002'),
           (belmeta, 'https://belmeta.com/vacansii?q=python&l=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA'))

jobs = []

for func, url in parsers:
    j = func(url)
    jobs += j

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

h = codecs.open('works.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()