from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from flowerapp.models import Bouquet, BouquetFlower
from django.core.paginator import Paginator


def index(request):
    recommended = Bouquet.objects.only('id','name','price','image','image_card').order_by('id')[:3]
    return render(request, 'index.html', {'recommended': recommended})


def catalog(request):
    qs = Bouquet.objects.only('id','name','price','image','image_card').order_by('id')
    page = Paginator(qs, 6).get_page(request.GET.get('page'))
    return render(request, 'catalog.html', {'page_obj': page})


def consultation(request): return render(request, 'consultation.html')

def card(request, bouquet_id):
    bf_qs = BouquetFlower.objects.select_related('flower')
    bouquet = get_object_or_404(
        Bouquet.objects.prefetch_related(
            Prefetch('bouquetflower_set', queryset=bf_qs),
            'additions',
        ),
        pk=bouquet_id
    )
    components = bouquet.bouquetflower_set.all()
    return render(request, 'card.html', {
        'bouquet': bouquet,
        'components': components,
    })


def order(request):
    bouquet_id = (
        request.GET.get('bouquet_id')
        or request.POST.get('bouquet_id')
        or request.session.get('order_data', {}).get('bouquet_id')
    )
    bouquet = Bouquet.objects.filter(pk=bouquet_id).first() if bouquet_id else None

    if request.method == 'POST':
        request.session['order_data'] = {
            'bouquet_id': bouquet_id,
            'client_name': request.POST.get('fname'),
            'client_phone': request.POST.get('tel'),
            'client_address': request.POST.get('adres'),
            'delivery_time': request.POST.get('orderTime'),
        }
        return redirect('order_step')

    return render(request, 'order.html', {
        'bouquet': bouquet,
        'order_data': request.session.get('order_data', {}),
    })


def order_step(request):
    order_data = request.session.get('order_data', {})
    if request.method == 'POST':
        order_data = request.session.get('order_data', {})
        if order_data:
            del request.session['order_data']
            #Вкорячить оплату
            return redirect('index')

    return render(request, 'order-step.html', {'order_data': order_data})

def quiz(request):
    #тут цикл из событий
    if request.method == 'POST':
        event = request.POST.get('event')
        request.session['quiz'] = {'event': event}
        return redirect('quiz_step')

    events = [
        {'id':1, 'name':'Свадьба'},
        {'id': 1, 'name': 'День рождения'},
        {'id': 1, 'name': 'Без повода'},
    ]
    return render(request, 'quiz.html', {'events': events})


def quiz_step(request):
    if request.method == 'POST':
        price = request.POST.get('price')
        kek = request.session.get('quiz')
        request.session['quiz'].update({'price': price})
        return redirect('result')
    return render(request, 'quiz-step.html')


def result(request):
    #Должна быть логика выбора
    bouquet_test = {
        "id": 1,
        # Здесь цикл для цветов, желательно отдельной функцией
        "flowers": """
            Гортензия розовая - 1 шт.\n
            Ветки эквалипта - 5 шт.\n
            Гипсофила - 1 шт.\n
            Матовая упаковка - 1 шт.\n
            Лента атласная - 1 шт.\n
            Рекомендация по уходу - 1 шт.\n
            Открыточка с вашими пожеланиями - 1 шт.\n
            Любовь флориста (бесплатно) - 1 шт.\n
            """,
            "price": 3700,
            "width": 30,
            "height": 40,
            "img": "img/catalog/catalogBg1.jpg"
    }
    return render(request, 'result.html', {"bouquet": bouquet_test})