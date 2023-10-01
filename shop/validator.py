from rest_framework import serializers


class RetailsValidator:
    """
    Валидатор уровня. Уровень 0 не имеет поставщиков.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self):
        if self.level == 'factory' and self.supplier is not None:
            message = 'Объект на уровне 0 не может иметь поставщиков!'
            raise serializers.ValidationError(message)
