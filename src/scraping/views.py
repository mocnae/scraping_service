from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from scraping.forms import FindForm
from scraping.models import Vacancy
from django.core.paginator import Paginator

user = get_user_model()


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

    qsb = Vacancy.objects.all()
    if not city and not language:
        qs = qsb
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['object_list'] = page_obj
    return render(request, 'list.html', context)


@login_required
def home_authorized(request):
    form = FindForm()
    user = request.user
    city = user.city
    language = user.language
    qs = Vacancy.objects.filter(city=city, language=language)
    return render(request, 'home_authorized.html', {'object_list': qs, 'form': form})
