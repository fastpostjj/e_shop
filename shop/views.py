from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.response import Response
from shop.models import Products, Retails
from shop.serializer import ProductsSerializers, RetailsSerializers
from shop.paginations import PaginationClass
from shop.permissions import IsActiveRequired


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductsSerializers
    pagination_class = PaginationClass
    permission_classes = [IsAuthenticated]
    queryset = Products.objects.all().order_by('name')


class RetailsViewSet(viewsets.ModelViewSet):
    serializer_class = RetailsSerializers
    pagination_class = PaginationClass
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']
    queryset = Retails.objects.all().order_by('name')


class AdminActionUpdateView(generics.UpdateAPIView):
    serializer_class = RetailsSerializers
    pagination_class = PaginationClass
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Retails.objects.all().order_by('name')

    def partial_update(self, request, *args, **kwargs):
        # Наши дополнительные проверки, преобразования и ограничения
        instance = self.get_object()
        instance.admin_action()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Ваш код для проведения необходимых проверок, преобразований и ограничений

        # Вызываем родительский метод partial_update для выполнения остальной работы
        self.perform_update(serializer)

        return Response(serializer.data)
