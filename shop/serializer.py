from rest_framework import serializers
from shop.models import Products, Retails
from shop.validator import RetailsValidator


class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            'name',
            'model',
            'date_market_launch'
        )


class RetailsSerializers(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        # Исключаем поле 'obligation' из обновления
        validated_data.pop('obligation', None)
        return super().update(instance, validated_data)

    def partial_update(self, instance, validated_data):
        # Исключаем поле 'obligation' из обновления
        validated_data.pop('obligation', None)
        return super().partial_update(instance, validated_data)

    class Meta:
        model = Retails
        fields = (
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
    validators = [RetailsValidator()]
