from django.shortcuts import render
from scraping.forms import FindForm
from scraping.models import Vacancy


def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        filter = {}
        if city:
            filter['city__slug'] = city
        if language:
            filter['language__slug'] = language
        qs = Vacancy.objects.filter(**filter)

    return render(request, 'home.html', {'object_list': qs, 'form': form})
