from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Event, Flower, Addition, Bouquet, BouquetFlower,
    Courier, Order, Consultation
)


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'client_phone', 'bouquet', 'status', 'courier', 'created_at')
    list_filter = ('status', 'courier', 'created_at')
    search_fields = ('client_name', 'client_phone', 'bouquet__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    autocomplete_fields = ('bouquet', 'courier')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('bouquet', 'courier')


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client_name', 'client_phone')
    readonly_fields = ('created_at',)
