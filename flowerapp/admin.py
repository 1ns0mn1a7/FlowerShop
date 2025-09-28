import csv
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count, F
from .models import (
    Event, Flower, Addition, Bouquet, BouquetFlower,
    Courier, Order, Consultation, ClickCounter
)


@admin.register(ClickCounter)
class ClickCounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'clicks', 'referral_link')
    readonly_fields = ('clicks', 'referral_link', 'token')
    search_fields = ('token',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ['clicks']

    def referral_link(self, obj):
        url = f"{settings.SITE_URL}/?ref={obj.token}"
        return format_html(
            '<input type="text" value="{}" readonly style="width: 300px;" onclick="this.select()">'
            '<br><a href="{}" target="_blank">Перейти по ссылке</a>',
            url, url
        )

    referral_link.short_description = "Реферальная ссылка"


class BouquetFlowerInline(admin.TabularInline):
    model = BouquetFlower
    extra = 1
    autocomplete_fields = ('flower',)
    fields = ('flower', 'quantity')
    

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    

@admin.register(Addition)
class AdditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_qty')
    search_fields = ('name',)
    
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'catalog_preview', 'card_preview', 'is_recommended')
    search_fields = ('name', 'description')
    list_editable = ('is_recommended',)
    list_filter = ('events', 'additions', 'is_recommended')
    readonly_fields = ('catalog_preview', 'card_preview')
    filter_horizontal = ('events', 'additions')
    inlines = [BouquetFlowerInline]

    @admin.display(description='Каталог')
    def catalog_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="height:60px;">', obj.image.url)
        return '—'

    @admin.display(description='Карточка')
    def card_preview(self, obj):
        if obj.image_card and hasattr(obj.image_card, 'url'):
            return format_html('<img src="{}" style="height:60px;">', obj.image_card.url)
        return '—'


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')


@admin.action(description='Экспорт выделенных в CSV')
def export_orders_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename="orders_{timezone.now():%Y%m%d_%H%M%S}.csv"'
    )
    response.write('\ufeff')
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Дата', 'Клиент', 'Телефон', 'Букет', 'Сумма', 'Статус'])
    
    for order in queryset.select_related('bouquet'):
        writer.writerow([
            order.id,
            order.created_at.strftime('%Y-%m-%d %H:%M'),
            order.client_name,
            order.client_phone,
            order.bouquet.name if order.bouquet_id else '',
            order.bouquet.price if order.bouquet_id else '',
            order.get_status_display(),
        ])

    return response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'client_phone', 'bouquet', 'status_display', 'courier', 'created_at')
    list_filter = (('created_at', admin.DateFieldListFilter), 'status', 'courier')
    search_fields = ('client_name', 'client_phone', 'bouquet__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    autocomplete_fields = ('bouquet', 'courier')
    actions = [export_orders_csv]

    @admin.display(description='Статус', ordering='status')
    def status_display(self, obj):
        return obj.get_status_display()

    def get_queryset(self, request):
        base_queryset = super().get_queryset(request)
        return base_queryset.select_related('bouquet', 'courier')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            change_list = response.context_data['cl']
            filtered_queryset = change_list.queryset.select_related('bouquet', 'courier')
        except Exception:
            return response

        total_orders = filtered_queryset.count()
        total_revenue = filtered_queryset.aggregate(total=Sum('bouquet__price'))['total'] or 0
        average_check = (total_revenue / total_orders) if total_orders else 0

        summary = {
            'orders': total_orders,
            'revenue': total_revenue,
            'avg_check': average_check,
        }

        status_labels = dict(Order.STATUS_CHOICES)
        by_status_queryset = (
            filtered_queryset
            .values('status')
            .annotate(orders=Count('id'), revenue=Sum('bouquet__price'))
            .order_by('status')
        )
        by_status = [
            {
                'label': status_labels.get(row['status'], row['status']),
                'orders': row['orders'],
                'revenue': row['revenue'],
            }
            for row in by_status_queryset
        ]

        top_bouquets = (
            filtered_queryset
            .values('bouquet_id', 'bouquet__name')
            .annotate(cnt=Count('id'), revenue=Sum('bouquet__price'))
            .order_by('-cnt')[:5]
        )

        response.context_data.update({
            'summary': summary,
            'by_status': by_status,
            'top_bouquets': list(top_bouquets),
        })
        return response


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client_name', 'client_phone')
    readonly_fields = ('created_at',)
