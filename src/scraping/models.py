from django.db import models

from scraping.utils import cirillic_to_eng


def default_urls():
    return {'rabota': '', 'belmeta': ''}


class City(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название населенного пункта',
                            unique=True)
    slug = models.CharField(blank=True, max_length=50)

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенного пункта'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = cirillic_to_eng(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Язык программирования',
                            unique=True)
    slug = models.CharField(blank=True, max_length=50)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = cirillic_to_eng(self.name)
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    title = models.CharField(max_length=70, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    company = models.CharField(max_length=70, verbose_name='Название компании')
    url = models.URLField(unique=True, verbose_name='Url')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ('timestamp',)

    def __str__(self):
        return self.title


class Url(models.Model):
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
