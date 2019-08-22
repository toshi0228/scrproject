from django.shortcuts import render
from django.http import HttpResponse
from .models import reviews, Yado
from .scrap import get
from .ja import jaget
from scrapingproject.settings import MEDIA_ROOT, MEDIA_URL

# Create your views here.

def index(request):
    # get()
    return HttpResponse('スクレイピング完了')

def rev(request):
    rev = reviews.objects.all()
    
    if request.method == 'GET':
        print("scraping開始します")
    else:
        print('scrapingしません')
    return render (request, 'index.html', {'rev': rev})



def scrap(request):
    if request.method == 'GET':
        print("scraping開始します")
    else:
        print('scrapingしません')
        
        
        
def finish(request):
    
    rev = reviews.objects.all()
    a = Yado.objects.all()
    
    if request.method == 'POST' or request.method == 'GET':
        get()
    else:
        print("あああ")
    return render (request, 'finish.html', {'rev': rev,
                                            'a':a})



def ja(request):
    
    rev = reviews.objects.all()
    
    if request.method == 'POST' or request.method == 'GET':
        jaget()
    else:
        print("あああ")
    return render (request, 'finish.html', {'rev': rev})