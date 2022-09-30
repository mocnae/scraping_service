from django.shortcuts import render
from scraping.forms import FindForm
from scraping.models import Vacancy
from django.core.paginator import Paginator


def home_view(request):
    form = FindForm()

    return render(request, 'home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        filter = {}
        if city:
            filter['city__slug'] = city
        if language:
            filter['language__slug'] = language
        qs = Vacancy.objects.filter(**filter)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    return render(request, 'list.html', context)
