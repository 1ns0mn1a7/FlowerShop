from django.shortcuts import render, get_object_or_404, redirect

from flowerapp.models import Bouquet, BouquetFlower


def index(request): return render(request, 'index.html')
def catalog(request): return render(request, 'catalog.html')
def consultation(request): return render(request, 'consultation.html')
def quiz(request): return render(request, 'quiz.html')
def quiz_step(request): return render(request, 'quiz-step.html')
def result(request): return render(request, 'result.html')


def card(request, bouquet_id):
    bouquet = get_object_or_404(
        Bouquet.objects.prefetch_related('flowers'),
        id=bouquet_id
        )

    bouquet_flowers = BouquetFlower.objects.filter(
        bouquet=bouquet).select_related("flower")

    bouquet_test = {
        "id": bouquet.id,
        "name": bouquet.name,
        "flowers": ''.join(
            f'{bouquet_flower.flower.name} - {bouquet_flower.quantity} шт.\n'
            for bouquet_flower in bouquet_flowers
            ),
        "price": bouquet.price,
        "width": bouquet.width,
        "height": bouquet.length,
        "img": bouquet.image.url
    }
    return render(request, 'card.html', {"bouquet": bouquet_test})


def order(request):
    bouquet_id = request.GET.get('bouquet_id')
    order_data = request.session.get('order_data', {})
    if request.method == 'POST':
        #Не придумал че вкорячить
        request.session['order_data'] = {
            'bouquet_id': bouquet_id,
            'client_name':request.POST.get('fname'),
            'client_phone': request.POST.get('tel'),
            'client_address': request.POST.get('adres'),
            'delivery_time': request.POST.get('orderTime')
        }
        return redirect('order_step')
    return render(request, 'order.html', {
        'bouquet': bouquet_id,
        'order_data': order_data
    })


def order_step(request):
    order_data = request.session.get('order_data', {})
    if request.method == 'POST':
        order_data = request.session.get('order_data', {})
        if order_data:
            del request.session['order_data']
            #Вкорячить оплату
            return redirect('result')

    return render(request, 'order-step.html', {'order_data': order_data})


def result(request):
    price = request.GET.get('price')
    event_id = request.GET.get('event.id')

    bouquets = Bouquet.objects.prefetch_related('flowers')
    if price:
        bouquets = bouquets.filter(price__lte=price)
    if event_id:
        bouquets = bouquets.filter(event__id=event_id)

    return render(request, 'result.html', {'bouquets': bouquets})
