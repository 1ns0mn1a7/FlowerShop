from django.shortcuts import render, get_object_or_404
from flowerapp.models import Bouquet, BouquetFlower


def index(request): return render(request, 'index.html')
def catalog(request): return render(request, 'catalog.html')


def card(request, bouquet_id=1):
    bouquet = get_object_or_404(
        Bouquet.objects.prefetch_related('flowers'),
        id=bouquet_id
        )

    serialized_bouqued = {
        'title': bouquet.name,
        'price': bouquet.price,
        'image': bouquet.image.url,
        'width': bouquet.width,
        'length': bouquet.length,
        'flowers': [
            {
                'name': bf.flower.name,
                'amount': bf.quantity
            } for bf in BouquetFlower.objects.filter(bouquet=bouquet)
        ]
    }
    return render(request, 'card.html', {'bouquet': serialized_bouqued})


def order(request): return render(request, 'order.html')
def order_step(request): return render(request, 'order-step.html')
def consultation(request): return render(request, 'consultation.html')
def quiz(request): return render(request, 'quiz.html')
def quiz_step(request): return render(request, 'quiz-step.html')
def result(request): return render(request, 'result.html')
