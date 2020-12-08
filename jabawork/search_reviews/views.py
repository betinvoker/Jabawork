from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, DetailView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Universities, Opinions

#   Список университетов
class MainPostList(View):
    def get(self, request):
        universities = Universities.objects.all()
        #   Пагинатор выбирает из таблицы Universities 10 университетов и выводит их на страницу
        paginator = Paginator(universities, 10)

        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, "search_reviews/index.html", context = {"page_obj" : page_obj})

#   Выбранный университет
class ReviewsDetailView(DetailView):
    model = Universities
    template_name = 'search_reviews/reviews.html'
    context_object_name = 'review'

    # Переопределение параметров ReviewsDetailView
    def get_context_data(self, *args, **kwargs): 
        context = super(ReviewsDetailView, 
             self).get_context_data(*args, **kwargs) 
        context["opinions"] = Opinions.objects.all().filter(university_id = ReviewsDetailView.get_object(self))       
        return context 