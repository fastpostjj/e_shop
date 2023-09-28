from django.contrib import admin
from shop.models import Products, Retails


@admin.register(Retails)
class RetailsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'level',
        'email',
        'country',
        'city',
        'street',
        'house_number',
        'product',
        'supplier',
        'obligation',
        'time_created'
    )
    list_display = (
        'name',
        'level',
        'email',
        'country',
        'city',
        'street',
        'house_number',
        'product',
        'supplier',
        'obligation',
        'time_created'
    )
    list_display = (
        'name',
        'level',
        'email',
        'country',
        'city',
        'street',
        'house_number',
        'product',
        'supplier',
        'obligation',
        'time_created'
    )
    search_fields = (
        'name',
        'level',
        'email',
        'country',
        'city',
        'street',
        'house_number',
        'product',
        'supplier',
        'obligation',
        'time_created'
    )


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display_links = (
            'name',
            'model',
            'date_market_launch'
    )

    list_filter = (
            'name',
            'model',
            'date_market_launch'

    )

    list_display = (
            'name',
            'model',
            'date_market_launch'
    )

    search_fields = (
            'name',
            'model',
            'date_market_launch'
    )
