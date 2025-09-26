from django.shortcuts import render

from flowerapp.models import Bouquet


def index(request): return render(request, 'index.html')
def catalog(request): return render(request, 'catalog.html')
def order(request): return render(request, 'order.html')
def order_step(request): return render(request, 'order-step.html')
def consultation(request): return render(request, 'consultation.html')
def quiz(request): return render(request, 'quiz.html')
def quiz_step(request): return render(request, 'quiz-step.html')
def result(request): return render(request, 'result.html')
def card(request, bouquet_id):
    # bouquet = Bouquet.objects.get(id=bouquet_id)
    bouquet_test = {
        "id":1,
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
        "price":3600,
        "width":30,
        "height":40,
        "img":"img/catalog/catalogBg1.jpg"
    }
    return render(request, 'card.html', {"bouquet": bouquet_test})