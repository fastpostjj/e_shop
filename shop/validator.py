from rest_framework import serializers


class RetailsValidator:
    """
    Валидатор уровня. Уровень 0 не имеет поставщиков.
    """

    def __call__(self, value):
        level = value.get('level')
        supplier = value.get('supplier')
        if level == 'factory' and supplier is not None:
            message = 'Объект на уровне 0 не может иметь поставщиков!'
            raise serializers.ValidationError(message)
