# FlowerShop

Мини-магазин букетов на Django. Админка с превью, «рекомендуемыми» букетами, карточкой товара, обратной формой для консультации, подбором букета, оформлением заказа и встроенной сводной статистикой в панели администратора с возможностью экспорта заказов в CSV.

## Стек
- Python 3.10+
- Django
- django-environ
- Pillow (для Изображений)
- DRF

## Быстрый старт

Создайте виртуальное окружение и установите зависимости:

```bash
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

Создайте `.env`:

```env
SECRET_KEY=your-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Миграции и админка:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Статика и медиа
- `STATIC_URL` = `/static/`, дев-статик лежит в `frontend/static`.
- `MEDIA_URL` = `/media/`, файлы - в `media/`.
- В `urls.py` проекта при `DEBUG=True` должны быть раздачи `static` и `media`. Если нет - добавьте:

```bash
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Прод: `python manage.py collectstatic` и настройка веб-сервера на `/static` и `/media`.

## Админка

Панель управления интернет-магазином доступна по пути `/admin`.

Возможности:
- Управление товарами, их атрибутами и свойствами.
- Управление заказами, статусами и назначение курьеров на их исполнение.
- Сбор имеи и номера телефона с формы обратной связи для консультации.
- Назначение по флажку `true` товаров для блока рекомендаций.
- Экспорт выделенных заказов в CSV
- Сводная статистика прямо над списком заказов:
    - KPI: заказы, выручка, средний чек
    - Статусы: кол-во и выручка по каждому статусу
    - Топ букетов: по числу заказов и выручке

Шаблон сводки: `frontend/templates/admin/change_list.html`

Если путь другой - скорректируйте `TEMPLATES['DIRS']` или расположение файла.

## Вёрстка и шаблоны

Страницы:
 - `/` - Главная страница, блок рекомендаций с контактами и картой расположения магазинов. Блок рекомендаций берез товары из `Bouquet is_recommended=True` в админ-панели.

 - `/catalog/` - каталог. Пагинация по 6 шт с кнопкой "Показать ещё", которая дозагружает ещё 6 карточек по нажатию в каталоге.

 - `/card/<id>/` - карточка товара. 

 - `/order` - оформление заказа. Передаём `?bouquet_id=<id>` из карточки.

 - `/order-step/` - шаг оплаты.

 - `/quiz/`, `/quiz-step/`, `/result/` - страницы подбора букета по параметрам.

 ## API

 ```bash
 /api/consultations/create/  # POST - создать заявку на консультацию
 ```

 ## Экспорт CSV

 В списке заказов выберите записи - «Экспорт выделенных в CSV». Файл скачается и откроется в Excel.

## Продакшн

- `DEBUG=False`, заполните `ALLOWED_HOSTS`.
- `collectstatic`.
- Настройте раздачу `/static/` и `/media/` веб-сервером.

