from django.shortcuts import render
from django.http import HttpResponse
from .models import reviews, Yado
from .scrap import get
from .ja import jaget
from .jaex import jaexget
from .rt import rtget
from .rtsa import rtsaget
from .rtnum import rtnum_get
from .janum import janum_get
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
    return render (request, 'index.html', {'rev': rev})


#じゃらんデータベースに保存
def ja(request):
    
    rev = reviews.objects.all()
    
    if request.method == 'POST' or request.method == 'GET':
        jaget()
    else:
        print("あああ")
    return render (request, 'finish.html', {'rev': rev})



#じゃらんエクセルにデータ保存
def jaex(request):
    # rev = reviews.objects.all()
    print(request.method)
    
    if request.method == 'POST' or request.method == 'GET':
        jaexget()
    else:
        print("エクセルに保存が動いた")
    return HttpResponse('エクセルにじゃらんの口コミデータ保存完了')


#楽天
def rt(request):
    if request.method == 'POST' or request.method == 'GET':
        rtget()
    return HttpResponse('エクセルに楽天の口コミデータ保存完了')



#楽天営業用エリア移動なし
def rtsa(request):
    if request.method == 'POST' or request.method == 'GET':
        rtsaget()
    return HttpResponse('エクセルに楽天の口コミデータ保存完了(営業用)')


#楽天営業用エリア番号取得
def rtnum(request):
    if request.method == 'POST' or request.method == 'GET':
        rtnum_get()
    return HttpResponse('楽天番号取得完了')

def janum(request):
    if request.method == 'POST' or request.method == 'GET':
        janum_get()
    return HttpResponse('じゃらん番号取得完了')
    
    
    