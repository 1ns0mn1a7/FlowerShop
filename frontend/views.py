import random
import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from flowerapp.models import Bouquet, BouquetFlower, Event, Flower, Addition, Order
from django.core.paginator import Paginator
from django.conf import settings

def index(request):
    queryset = Bouquet.objects.only('id','name','price','image','image_card','is_recommended')
    recommended = queryset.filter(is_recommended=True).order_by('id')[:3]
    return render(request, 'index.html', {'recommended': recommended})


def catalog(request):
    queryset = Bouquet.objects.only('id','name','price','image','image_card').order_by('id')
    page = Paginator(queryset, 6).get_page(request.GET.get('page'))
    return render(request, 'catalog.html', {'page_obj': page})


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
        request.session['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return redirect('order_step')

    return render(request, 'order.html', {
        'bouquet': bouquet,
        'order_data': request.session.get('order_data', {}),
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })


def order_step(request):
    #4242 4242 4242 4242
    stripe.api_key = settings.STRIPE_SECRET_KEY
    order_data = request.session.get('order_data', {})

    context = {
        'order_data': order_data,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    }

    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            bouquet = Bouquet.objects.get(id=order_data.get('bouquet_id'))
            print(order_data)
            intent = stripe.PaymentIntent.create(
                amount=int(bouquet.price * 100),
                currency='rub',
                payment_method=token,
                confirm=True,
                description=f"Оплата букета: {bouquet.name}",
                return_url=request.build_absolute_uri('/order-success/'),
                payment_method_types=['card'],
            )

            if intent.status == 'requires_action':
                return render(request, 'order-step.html', {
                    'order_data': order_data,
                    'client_secret': intent.client_secret,
                    'requires_action': True
                })
            elif intent.status == 'succeeded':
                Order.objects.create(
                    bouquet=bouquet,
                    client_name=order_data.get('client_name'),
                    client_phone=order_data.get('client_phone'),
                    #Нужна дата
                    # client_address=order_data.get('client_address'),
                    delivery_time=order_data.get('delivery_time'),
                    status='accepted'
                )

                if order_data:
                    del request.session['order_data']
                return redirect('index')

            else:
                return render(request, 'order-step.html', {
                    'order_data': order_data,
                    'error': f'Не удалось обработать платеж. Статус: {intent.status}'
                })

        except stripe.error.StripeError as e:
            context['error'] = f'Ошибка оплаты: {str(e)}'
            return render(request, 'order-step.html', context)
        except Bouquet.DoesNotExist:
            context['error'] = 'Букет не найден'
            return render(request, 'order-step.html', context)
        except Exception as e:
            context['error'] = f'Произошла ошибка: {str(e)}'
            return render(request, 'order-step.html', context)

    return render(request, 'order-step.html', context)

def quiz(request):
    #тут цикл из событий
    if request.method == 'POST':
        event = request.POST.get('event')
        request.session['quiz'] = {'event': event}
        request.session.modified = True
        return redirect('quiz_step')

    events = Event.objects.all().values("id", "name")
    return render(request, 'quiz.html', {'events': events})


def quiz_step(request):
    if request.method == 'POST':
        price = request.POST.get('price')
        quiz_data = request.session.get('quiz', {})
        quiz_data['price'] = price
        request.session['quiz'] = quiz_data
        request.session.modified = True
        return redirect('result')
    return render(request, 'quiz-step.html')


def result(request):
    data = request.session.get('quiz')
    event_id = data['event']
    price_id =data['price']

    bouquets_query = Bouquet.objects.filter(events__id=event_id).distinct()

    bouquet_flowers_prefetch = Prefetch(
        'bouquetflower_set',
        queryset=BouquetFlower.objects.select_related('flower'),
        to_attr='flower_items'
    )
    additions_prefetch = Prefetch(
        'additions',
        queryset=Addition.objects.all(),
        to_attr='addition_items'
    )

    match price_id:
        case '1':
            filtered = bouquets_query.filter(price__lt=1000)
        case '2':
            filtered = bouquets_query.filter(price__range=(1000, 5000))
        case '3':
            filtered = bouquets_query.filter(price__gt=5000)
        case '4':
            filtered = bouquets_query

    if not filtered.exists():
        filtered = bouquets_query

    final_bouquets = filtered.prefetch_related(
        bouquet_flowers_prefetch,
        additions_prefetch
    )

    bouquet_list = []
    for bouquet in final_bouquets:
        flowers_lines = [
            f"{bf.flower.name} - {bf.quantity} шт."
            for bf in bouquet.bouquetflower_set.all()
        ]
        additions_lines = [
            f"{addition.name} - {addition.default_qty} шт."
            for addition in bouquet.additions.all()
        ]
        all_lines = flowers_lines + additions_lines
        full_composition = "\n".join(all_lines) + "\n"
        bouquet_data = {
            "id": bouquet.id,
            "name": bouquet.name,
            "flowers": full_composition,
            "price": int(bouquet.price),
            "width": float(bouquet.width),
            "height": float(bouquet.length),
            "img": bouquet.image.url if bouquet.image else "",
            "description": bouquet.description
        }
        bouquet_list.append(bouquet_data)

    selected_bouquet = random.choice(bouquet_list) if bouquet_list else None
    return render(request, 'result.html', {"bouquet": selected_bouquet})