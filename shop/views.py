from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.response import Response
from shop.models import Products, Retails
from shop.serializer import ProductsSerializers, RetailsSerializers
from shop.paginations import PaginationClass
from drf_yasg.utils import swagger_auto_schema


class ProductsViewSet(viewsets.ModelViewSet):
    """
    Представление для модели Products
    """
    serializer_class = ProductsSerializers
    pagination_class = PaginationClass
    permission_classes = [IsAuthenticated]
    queryset = Products.objects.all().order_by('name')


class RetailsViewSet(viewsets.ModelViewSet):
    """
    Представление для модели Retails
    """
    serializer_class = RetailsSerializers
    pagination_class = PaginationClass
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'city']
    queryset = Retails.objects.all().order_by('name')


class AdminActionUpdateView(generics.UpdateAPIView):
    """
    Представление для выполнения метода admin_action
    для обнуления задолженности поставщику.
    Доступно только админу.
    """
    serializer_class = RetailsSerializers
    pagination_class = PaginationClass
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Retails.objects.all().order_by('name')

    @swagger_auto_schema(
            operation_description="PATCH /admin_action/{id}/",
            responses={
                200: RetailsSerializers,
                400: 'Bad Request',
                401: 'Unauthorized',
                403: 'Forbidden',
                404: 'Not Found'
            }
            )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.admin_action()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
